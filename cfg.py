# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.8 (tags/v3.6.8:3c6b436a57, Dec 24 2018, 00:16:47) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: cfg.py
"""配置文件"""
ROOT_DIR = 'resources'
ACTION_DISTRIBUTION = [['1', '2', '3'],
 [
  '4', '5', '6', '7', '8', '9', '10', '11'],
 [
  '12', '13', '14'],
 [
  '15', '16', '17'],
 [
  '18', '19'],
 [
  '20', '21'],
 [
  '22'],
 [
  '23', '24', '25'],
 [
  '26', '27', '28', '29'],
 [
  '30', '31', '32', '33'],
 [
  '34', '35', '36', '37'],
 [
  '38', '39', '40', '41'],
 [
  '42', '43', '44', '45', '46']]
PET_ACTIONS_MAP = {'pet_1': ACTION_DISTRIBUTION}
for i in range(2, 65):
    PET_ACTIONS_MAP.update({'pet_%s' % i: ACTION_DISTRIBUTION})
# okay decompiling cfg.pyc
