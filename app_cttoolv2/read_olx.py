import logging
import os

from bs4 import BeautifulSoup
from django.conf import settings

from app_cttoolv2.filesystem import get_configuration

logger = logging.getLogger()


class OLXReader:
    """
    This class travels through whole input tar file and
    fetches course data and modifying the LTIs besides.
    """
    def __init__(self):
        self.vds_cnt = 0
        self.lti_cnt = 0

    def traverse_workspace(self, path):
        """
        Traverses the directory structure of the unpacked .tar.gz file.
        Inputs:
            path: Path to root of unpacked file.
        """
        course_detail = {}
        course_metadata = {}
        course_outline = []

        base_path = str(path) + '/' + os.listdir(str(path))[0] + '/'
        course_tree = get_course_tree(path, len(base_path))

        if settings.COURSE_XML in course_tree.get('course'):
            file_full_path = os.path.join(base_path+'course/', settings.COURSE_XML)
            course_detail = parse_course_xml(file_full_path)
            if (
                'course_url' in course_detail and
                course_detail['course_url'] + '.xml' in
                course_tree.get('course/course')
               ):
                file_full_path = os.path.join(
                    base_path+'course/course',
                    course_detail['course_url'] + '.xml'
                )
                course_metadata = parse_course_url_xml(file_full_path)
            if 'course/chapter' in course_tree:
                file_full_path = os.path.join(base_path+'course/')
                course_outline = self._traverse_course_content(file_full_path)

        logger.info('Total LTIs converted : %s', self.lti_cnt)
        logger.info('VDS LTIs converted : %s', self.vds_cnt)
        return {
            'course_metadata': course_metadata,
            'course_outline': course_outline,
            'base_path': base_path,
            'course_key_tags': course_detail
        }

    def _traverse_course_content(self, course_path):
        """
        Traverses through course content(e.g. section, subsection and unit).
        Inputs:
            course_path: path to course directory.
        """
        sequentials = os.listdir(str(course_path+'sequential'))
        sequential_list = []
        for sequential in sequentials:
            sequential_list.append(
                self.parse_sequential_xml(sequential, course_path)
            )
        return sequential_list

    def parse_sequential_xml(self, seq_name, course_path):
        """
        Parse the <sequential>.xml and extract vertical tags.
        Inputs:
            seq_name: name of sequential xml file.
            course_path: path to course directory.
        """
        sequntial_path = course_path + 'sequential/' + seq_name
        with open(sequntial_path, 'r', encoding='utf-8') as seq_xml_file:
            data = seq_xml_file.read()

        bs_data = BeautifulSoup(data, 'xml')
        vertical_list = []
        seq_display_name = bs_data.find('sequential').get("display_name")
        verticals = bs_data.find_all('vertical')
        for vertical in verticals:
            vertical_name = vertical.get('url_name') + '.xml'
            vertical_list.append(
                self.parse_vertical_xml(
                    vertical_name,
                    course_path
                )
            )
        return {
            "seq_display_name": seq_display_name,
            "verticals": vertical_list
        }

    def parse_vertical_xml(self, vertical_name, course_path):
        pass


def get_course_tree(path, base_path_len):
    """
    Returns a dict of lists having directory(key) and list of file(value).
    Inputs:
        path: Path to root of unpacked file.
        base_path_len: length of base path.
    """
    course_tree = {}
    # pylint: disable=unused-variable
    for root, dir_names, file_names in os.walk(str(path)):
        if file_names:
            course_tree[root[base_path_len:]] = file_names
    return course_tree


def parse_course_xml(course_xml):
    """
    Parse the course.xml file and extract attributes.
    Inputs:
        course_xml: course_xml file.
    """
    with open(course_xml, 'r', encoding='utf-8') as course_xml_file:
        data = course_xml_file.read()

    bs_data = BeautifulSoup(data, 'xml')

    course_tag = bs_data.find('course')
    course = course_tag.get('course')
    org = course_tag.get('org')
    url_name = course_tag.get('url_name')

    logger.info('course_tag_attributes: %s %s %s', course, org, url_name)
    return {
        'course_run': course,
        'course_org': org,
        'course_url': url_name
    }


def parse_course_url_xml(course_url_path):
    """
    Parse the <course_url_name>.xml and extract course details like name.
    Inputs:
        course_url_path: Path to course url file.
    """
    with open(course_url_path, 'r', encoding='utf-8') as course_url_file:
        data = course_url_file.read()

    bs_data = BeautifulSoup(data, 'xml')

    course_tag = bs_data.find('course')
    display_name = course_tag.get('display_name')
    course_start = course_tag.get('start')
    course_conclude = course_tag.get('conclude')

    logger.info('course_name: %s', display_name)
    return {
        'display_name': display_name,
        'course_start': course_start,
        'course_conclude': course_conclude
    }
