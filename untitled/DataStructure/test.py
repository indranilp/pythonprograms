import typing
import aira_parsing.lib.aira_utils as utils
from aira_parsing.data_sources.crawler import Crawler
import datetime
import os
import requests


class SupportForumsCrawler(Crawler):
    today = datetime.datetime.now()
    tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)

    def __init__(self, name, local_conf_file='/etc/aira/supportforums.yml'):
        super().__init__(name, local_conf_file)

    def run(self):
        self.__parse()

    def get_id(self, item):
        id_ = item[".id"][0].split("/")[-1]
        return id_

    def check_response(self, response, board_name):
        if response.status_code == 200:
            self.script_logger.info(
                f"parsing, saving, and updating records for {board_name}")
            for item in response.json():
                try:
                    id_ = self.get_id(item)
                    self.script_logger.debug(f"handling sf ID {id_}")
                    self.expand_flattened_keys(item)
                    meta_data = self.parse_json(item)
                    utils.update_mongodb(
                        self.config, meta_data, self.mongo_connection)
                    self.save_data(item)
                except Exception as error:
                    self.script_logger.exception(f"encountered {error} while parsing {id_}")
            self.script_logger.info(f"finished parse of data for {board_name}")
        else:
            self.script_logger.error(f"query returned status code {response.status_code}, "
                                     f"response: {response.content}")

    def __parse(self):
        """ Query and fetch data for all board name in config.
        Check query response and for 200 response code
        Parse json response, update mongodab and save data """
        utils.assure_path_exists(self.config.data_dir)
        for board_name in self.config.board_names:
            self.script_logger.info(f"fetching data for {board_name}...")
            response = self.query_board(board_name)
            self.check_response(response, board_name)

    def delete_keys(self, json_data):
        del json_data[".id"]
        del json_data[".score"]
        del json_data[".zone"]

    def get_srs(self, id_, json_data, file_content):
        mentioned_srs = []
        try:
            mentioned_srs = utils.extract_sr_mentions(file_content)
        except Exception:
            self.script_logger.exception(f"failed to extract mentioned cases "
                                         f"from {id_} body content.")
        finally:
            json_data['srMentions'] = json_data.get(
                'srMentions', []) + mentioned_srs
        return mentioned_srs

    def get_bugs(self, id_, json_data, file_content):
        mentioned_bugs = []
        try:
            mentioned_bugs = utils.extract_cdets_mentions(file_content)
        except Exception:
            self.script_logger.exception(f"failed to extract mentioned bugs "
                                         f"from {id_} body content.")
        finally:
            json_data['bugMentions'] = json_data.get(
                'bugMentions', []) + mentioned_bugs
        return mentioned_bugs

    def get_tz_data(
            self,
            id_,
            json_data,
            file_content,
            mentioned_srs,
            mentioned_bugs):
        mentioned_tz_ids = []
        mentioned_urls = []
        non_tz_urls = []
        parse_config = self.config.parse_config

        try:
            present_ids = [id_] + mentioned_srs + mentioned_bugs
            ignore_strings = present_ids + parse_config['url_exclude_strings']
            mentioned_urls = utils.extract_url_mentions(
                file_content, ignore_strings)
        except Exception:
            self.script_logger.exception(f"failed to extract mentioned urls "
                                         f"from {id_} body content.")
        try:
            mentioned_tz_ids, non_tz_urls = utils.extract_tz_mentions(
                mentioned_urls)
        except Exception:
            self.script_logger.exception(f"failed to extract mentioned tz ids "
                                         f"from {id_} body content.")
            non_tz_urls = mentioned_urls
        finally:
            json_data['urlMentions'] = json_data.get(
                'urlMentions', []) + non_tz_urls
            json_data['tzMentions'] = json_data.get(
                'tzMentions', []) + mentioned_tz_ids

    def extract_data(self, id_, json_data, file_content):
        mentioned_srs = self.get_srs(id_, json_data, file_content)
        mentioned_bugs = self.get_bugs(id_, json_data, file_content)
        self.get_tz_data(
            id_,
            json_data,
            file_content,
            mentioned_srs,
            mentioned_bugs)

    def parse_json(self, json_data):
        """Parse json output from query and get srs, bugs"""
        parse_config = self.config.parse_config
        id_ = self.get_id(json_data)
        self.delete_keys(json_data)
        json_data["id"] = id_

        file_content = ""
        if json_data.get('text', ''):
            file_content = json_data.get('text', '')[0]
        if json_data.get('csclinear', ''):
            file_content += "\n" + json_data.get('csclinear', '')[0]
        for name in parse_config.get('string_to_list', {}):
            content = json_data.get(name, '')
            if content != '':
                delimiter = parse_config['string_to_list'].get(name, ',')
                if name == 'referredtzarticles':
                    referred_tz_articles = utils.string_to_list(
                        content, delimiter)
                    tz_ids, _ = utils.extract_tz_mentions(referred_tz_articles)
                    json_data['referredtzarticles'] = tz_ids
                else:
                    json_data[name] = utils.string_to_list(content, delimiter)
            self.extract_data(id_, json_data, file_content)

        return json_data

    def expand_flattened_keys(self, json_data):
        """ Expand key in json response"""
        for key, value in json_data.items():
            if r"." in key and key[0] != r".":
                self.script_logger.debug(f"expanding flattened key {key}...")
                del json_data[key]
                split_key = key.split(r".")
                first_key = split_key[0]
                final_key = split_key[-1]
                sub_dict = []
                for sub_key in split_key:
                    if sub_key == first_key:
                        json_data[first_key] = dict()
                        sub_dict = json_data[first_key]
                    elif sub_key == final_key:
                        sub_dict[final_key] = value
                    else:
                        sub_dict[sub_key] = dict()
                        sub_dict = sub_dict[sub_key]

    def run_query(self, query) :
        url = "https://searchapi.cloudapps.cisco.com/streaming/rest/stream/post"
        data = {
            "key": "d5a71f0904",
            "query": query,
            "format": "json",
            "queryLanguage": "ADVANCED",
            "fields": "*"
        }

        headers = {'Content-type': 'application/json'}
        response = requests.post(url, json=data, headers=headers)
        self.script_logger.info(
            "query returned status code {}".format(response.status_code))
        if response.status_code != 200:
            self.ob1.log(process='crawler',
                         process_id=f'{self.tech}-supportforums-crawler',
                         message=f'ERROR:{self.tech} supportforums crawler script '
                         f'query returned resposne {response.__dict__}.',
                         spark=True)
        return response

    def get_start_end_date(self) -> (str, str):
        if self.config.incremental_update:
            end_date = self.tomorrow
            start_date = self.end_date - datetime.timedelta(days=self.config.num_days)
        else:
            if self.config.end_date:
                end_date = datetime.datetime.strptime(self.config.end_date, self.date_format)
            else:
                end_date = self.tomorrow

            if self.config.start_date:
                start_date = datetime.datetime.strptime( self.config.start_date, self.date_format)
            else:
                start_date = end_date - datetime.timedelta(days=self.config.num_days)

        start_date = start_date.strftime(self.date_format)
        end_date = end_date.strftime(self.date_format)

        return (start_date, end_date)

    def generate_query(self, board_name: str) -> str:
        """
        Generate a query to be executed against Support Forums.

        board_name -- Support Forums board we are querying.
        """
        query: str
        board_id = f"cscboardid:{board_name}"

        if self.config.parse_all:
            query = board_id
        else:
            start_date, end_date = self.get_start_end_date()

            last_mod_lower = f"csclastmodified:>{start_date}"
            last_mod_upper = f"csclastmodified:<{end_date}"

            query = f"AND({board_id},{last_mod_lower},{last_mod_upper})"

        return query

    def query_board(self, board_name):
        """Rest api post request to get data for board"""
        self.script_logger.info(f"querying {board_name}...")

        query = self.generate_query(board_name)

        self.script_logger.debug(f"query: {query}")

        return self.run_query(query)

    def save_data(self, json_data):
        """ Save josn data from api response in file"""
        id_ = json_data["id"]
        self.script_logger.debug(f"saving file content for id {id_}...")
        file_content = ""
        if json_data.get('text', ''):
            file_content = json_data.get('text', '')[0]
        if json_data.get('csclinear', ''):
            file_content += "\n" + json_data.get('csclinear', '')[0]
        file_path = os.path.join(self.config.data_dir, f'{id_}.txt')
        with open(file_path, 'w') as f:
            f.write(file_content)
        self.script_logger.debug("file content saved successfully")
