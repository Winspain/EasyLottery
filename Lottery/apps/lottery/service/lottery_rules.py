# -- coding utf-8 --
# @Time     2022/10/8 16:07
# @Author   dicardo
# @File     lottery_rules.py
# @Software PyCharm

def lottery_rule(front, back):
    select_value = [front, back]
    prize_dict = {
        'first_prize': [5, 2],
        'second_prize': [5, 1],
        'third_prize': [5, 0],
        'fourth_prize': [4, 2],
        'fifth_prize': [4, 1],
        'sixth_prize': [3, 2],
        'seventh_prize': [4, 0],
        'eighth_prize_1': [3, 1],
        'eighth_prize_2': [2, 2],
        'ninth_prize_1': [3, 0],
        'ninth_prize_2': [1, 2],
        'ninth_prize_3': [2, 1],
        'ninth_prize_4': [0, 2],
    }
    prize_trans_dict = {
        'first_prize': '一等奖',
        'second_prize': '二等奖',
        'third_prize': '三等奖',
        'fourth_prize': '四等奖',
        'fifth_prize': '五等奖',
        'sixth_prize': '六等奖',
        'seventh_prize': '七等奖',
        'eighth_prize_1': '八等奖',
        'eighth_prize_2': '八等奖',
        'ninth_prize_1': '九等奖',
        'ninth_prize_2': '九等奖',
        'ninth_prize_3': '九等奖',
        'ninth_prize_4': '九等奖',
    }
    prize_values_list = list(prize_dict.values())
    if select_value in prize_values_list:
        select_index = list(prize_dict.values()).index(select_value)
        select_key = list(prize_dict.keys())[select_index]
        return prize_trans_dict[select_key]
    else:
        return '未中奖'


def lottery_compare(select_list, draw_list):
    """
    比较开奖号和个人选择
    :param select_list: 个人选择列表
    :type select_list:
    :param draw_list: 开奖列表
    :type draw_list:
    :return:
    :rtype:
    """
    select_list_front = select_list[0:5]
    select_list_back = select_list[5:7]
    draw_list_front = draw_list[0:5]
    draw_list_back = draw_list[5:7]
    front_number = len(set(select_list_front) & set(draw_list_front))
    back_number = len(set(select_list_back) & set(draw_list_back))
    return front_number, back_number
