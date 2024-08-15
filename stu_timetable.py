import streamlit as st
import requests
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime
import openpyxl

#학생데이터 하드코딩
student_data = {'2101': ['2학년 - 1', 'C3 선택', 'C2 선택', '창의 융합'],
 '2102': ['2학년 - 1', 'C3-AB 선택', 'C4 선택', 'C3-CD 선택', 'C2 선택', '창의 융합'],
 '2103': ['2학년 - 1', 'C3-AB 선택', 'C2 선택', '창의 융합'],
 '2104': ['2학년 - 1', 'C2 선택', 'C4 선택', '창의 융합'],
 '2105': ['2학년 - 1', 'C3-AB 선택', 'C2 선택', '창의 융합'],
 '2106': ['2학년 - 1', 'C3 선택', 'C4 선택', 'C2 선택', '창의 융합'],
 '2107': ['2학년 - 1', 'C3-AB 선택', 'C2 선택', '창의 융합'],
 '2108': ['2학년 - 1', 'C3-AB 선택', 'C4 선택', 'C2 선택', '창의 융합'],
 '2109': ['2학년 - 1', 'C4 선택', '창의 융합'],
 '2110': ['2학년 - 1', 'C2 선택', 'C4 선택', '창의 융합'],
 '2111': ['2학년 - 1', 'C3-AB 선택', 'C2 선택', '창의 융합'],
 '2112': ['2학년 - 1', 'C2 선택', 'C4 선택', '창의 융합'],
 '2113': ['2학년 - 1', 'C2 선택', 'C3-CD 선택', 'C4 선택', '창의 융합'],
 '2114': ['2학년 - 1', 'C2 선택', 'C4 선택', '창의 융합'],
 '2115': ['2학년 - 1', 'C3-AB 선택', 'C2 선택'],
 '2116': ['2학년 - 1', 'C3-AB 선택', 'C2 선택', '창의 융합'],
 '2201': ['2학년 - 2', 'C1 선택', 'C3 선택', 'C5 선택', '창의 융합'],
 '2202': ['2학년 - 2', 'C1 선택', 'C3 선택', 'C5 선택', '창의 융합'],
 '2203': ['2학년 - 2', 'C1 선택', 'C3-CD 선택', 'C5 선택', '창의 융합'],
 '2204': ['2학년 - 2', 'C1 선택', 'C3 선택', 'C5 선택', '창의 융합'],
 '2205': ['2학년 - 2', 'C1 선택', 'C3-AB 선택', 'C5 선택', '창의 융합'],
 '2206': ['2학년 - 2', 'C1 선택', 'C3-CD 선택', 'C5 선택', '창의 융합'],
 '2207': ['2학년 - 2', 'C5 선택', 'C1-AB 선택', 'C3 선택', '창의 융합'],
 '2208': ['2학년 - 2', 'C5 선택', 'C1-AB 선택', 'C3 선택', '창의 융합'],
 '2209': ['2학년 - 2', 'C1 선택', 'C3-AB 선택', 'C5 선택', '창의 융합'],
 '2210': ['2학년 - 2', 'C1 선택', 'C5 선택', 'C3 선택', '창의 융합'],
 '2211': ['2학년 - 2', 'C5 선택', 'C3 선택', 'C1 선택', '창의 융합'],
 '2212': ['2학년 - 2', 'C1 선택', 'C3-AB 선택', 'C5 선택', '창의 융합'],
 '2213': ['2학년 - 2', 'C1 선택', 'C3-AB 선택', 'C5 선택', '창의 융합'],
 '2214': ['2학년 - 2', 'C1 선택', 'C3 선택', 'C5 선택'],
 '2215': ['2학년 - 2', 'C3 선택', 'C1-AB 선택', 'C5 선택', '창의 융합'],
 '2301': ['2학년 - 3', 'C4 선택', 'C1 선택', 'C5 선택', '창의 융합'],
 '2302': ['2학년 - 3', 'C5 선택', 'C4 선택', 'C1 선택', '창의 융합'],
 '2303': ['2학년 - 3', 'C5 선택', 'C4 선택', 'C1 선택', '창의 융합'],
 '2304': ['2학년 - 3', 'C5 선택', 'C4 선택', 'C1 선택', '창의 융합'],
 '2305': ['2학년 - 3', 'C3 선택', 'C4 선택', 'C1-AB 선택', 'C5 선택', '창의 융합'],
 '2306': ['2학년 - 3', 'C5 선택', 'C4 선택', 'C1 선택', '창의 융합'],
 '2307': ['2학년 - 3', 'C3 선택', 'C1-AB 선택', 'C4 선택', '창의 융합'],
 '2308': ['2학년 - 3', 'C1 선택', 'C5 선택', 'C3 선택', '창의 융합'],
 '2309': ['2학년 - 3', 'C3 선택', 'C1-AB 선택', 'C4 선택', '창의 융합'],
 '2310': ['2학년 - 3', 'C5 선택', 'C1-AB 선택', 'C3 선택', '창의 융합'],
 '2311': ['2학년 - 3', 'C3 선택', 'C1-AB 선택', 'C5 선택', '창의 융합'],
 '2312': ['2학년 - 3', 'C5 선택', 'C1-AB 선택', 'C3 선택', '창의 융합'],
 '2313': ['2학년 - 3', 'C3 선택', 'C1-AB 선택', 'C5 선택', '창의 융합'],
 '2314': ['2학년 - 3', 'C3 선택', 'C5 선택', 'C4 선택', '창의 융합'],
 '2315': ['2학년 - 3', 'C1 선택', 'C4 선택', 'C5 선택', '창의 융합'],
 '2316': ['2학년 - 3', 'C3 선택', 'C1-AB 선택', 'C5 선택', '창의 융합'],
 '2401': ['2학년 - 4', 'C3 선택', 'C1 선택', 'C2 선택', '창의 융합'],
 '2402': ['2학년 - 4', 'C3 선택', 'C2 선택', 'C1-AB 선택', 'C4 선택', '창의 융합'],
 '2403': ['2학년 - 4', 'C2 선택', 'C1-AB 선택', 'C3 선택', 'C4 선택', '창의 융합'],
 '2404': ['2학년 - 4', 'C3 선택', 'C4 선택', 'C1 선택', 'C2 선택', '창의 융합'],
 '2405': ['2학년 - 4', 'C2 선택', 'C1 선택', 'C3-CD 선택', 'C4 선택', '창의 융합'],
 '2406': ['2학년 - 4', 'C4 선택', 'C3 선택', 'C1-AB 선택', 'C2 선택', '창의 융합'],
 '2407': ['2학년 - 4', 'C2 선택', 'C3-AB 선택', 'C1 선택', 'C3-CD 선택', 'C4 선택', '창의 융합'],
 '2408': ['2학년 - 4', 'C4 선택', 'C3 선택', 'C1 선택', 'C2 선택', '창의 융합'],
 '2409': ['2학년 - 4', 'C3 선택', 'C4 선택', 'C1 선택', 'C2 선택'],
 '2410': ['2학년 - 4', 'C2 선택', 'C1 선택', 'C3-CD 선택', 'C4 선택', '창의 융합'],
 '2411': ['2학년 - 4', 'C3 선택', 'C1 선택', 'C2 선택', '창의 융합'],
 '2412': ['2학년 - 4', 'C2 선택', 'C1 선택', 'C3-CD 선택', 'C4 선택', '창의 융합'],
 '2413': ['2학년 - 4', 'C2 선택', 'C1 선택', 'C3-CD 선택', 'C4 선택', '창의 융합'],
 '2414': ['2학년 - 4', 'C2 선택', 'C3-CD 선택', 'C4 선택', 'C1 선택', '창의 융합'],
 '2415': ['2학년 - 4', 'C2 선택', 'C3-CD 선택', 'C4 선택', 'C1 선택', '창의 융합'],
 '2416': ['2학년 - 4', 'C3 선택', 'C1-AB 선택', 'C2 선택', 'C4 선택', '창의 융합'],
 '2501': ['2학년 - 5', 'C3 선택', 'C5 선택', 'C2 선택', '창의 융합'],
 '2502': ['2학년 - 5', 'C2 선택', 'C3-AB 선택', 'C4 선택', '창의 융합'],
 '2503': ['2학년 - 5', 'C3 선택', 'C4 선택', 'C5 선택', 'C2 선택'],
 '2504': ['2학년 - 5', 'C5 선택', 'C4 선택', 'C3 선택'],
 '2505': ['2학년 - 5', 'C5 선택', 'C4 선택', 'C3 선택', '창의 융합'],
 '2506': ['2학년 - 5', 'C4 선택', 'C5 선택', 'C3 선택', 'C2 선택', '창의 융합'],
 '2507': ['2학년 - 5', 'C2 선택', 'C3-CD 선택', 'C5 선택', 'C4 선택', '창의 융합'],
 '2508': ['2학년 - 5', 'C5 선택', 'C4 선택', 'C2 선택', '창의 융합'],
 '2509': ['2학년 - 5', 'C2 선택', 'C5 선택', 'C3-AB 선택'],
 '2510': ['2학년 - 5', 'C2 선택', 'C4 선택', 'C3 선택', 'C5 선택', '창의 융합'],
 '2511': ['2학년 - 5', 'C2 선택', 'C5 선택', 'C4 선택', '창의 융합'],
 '2512': ['2학년 - 5', 'C3 선택', 'C5 선택', 'C2 선택', '창의 융합'],
 '2513': ['2학년 - 5', 'C3 선택', 'C4 선택', 'C5 선택', '창의 융합'],
 '2514': ['2학년 - 5', 'C3 선택', 'C5 선택', 'C2 선택', '창의 융합'],
 '2515': ['2학년 - 5', 'C3 선택', 'C5 선택', 'C2 선택', '창의 융합'],
 '2601': ['2학년 - 6', 'C3 선택', 'C2 선택', 'C4 선택', 'C1 선택', '창의 융합'],
 '2602': ['2학년 - 6', 'C1 선택', 'C4 선택', 'C3 선택', 'C2 선택', '창의 융합'],
 '2603': ['2학년 - 6', 'C1 선택', 'C3 선택', 'C2 선택', '창의 융합'],
 '2604': ['2학년 - 6', 'C2 선택', 'C3 선택', 'C4 선택'],
 '2605': ['2학년 - 6', 'C4 선택', 'C3 선택', 'C1 선택', 'C2 선택', '창의 융합'],
 '2606': ['2학년 - 6', 'C2 선택', 'C4 선택', 'C3 선택', '창의 융합'],
 '2607': ['2학년 - 6', 'C3 선택', 'C4 선택', 'C2 선택', '창의 융합'],
 '2608': ['2학년 - 6', 'C4 선택', 'C3 선택', 'C2 선택', '창의 융합'],
 '2609': ['2학년 - 6', 'C3 선택', 'C4 선택', 'C2 선택', '창의 융합'],
 '2610': ['2학년 - 6', 'C2 선택', 'C4 선택', 'C3 선택', '창의 융합'],
 '2611': ['2학년 - 6', 'C3 선택', 'C2 선택', 'C4 선택', '창의 융합'],
 '2612': ['2학년 - 6', 'C2 선택', 'C4 선택', 'C3 선택', '창의 융합'],
 '2613': ['2학년 - 6', 'C4 선택', 'C2 선택', 'C3 선택'],
 '2614': ['2학년 - 6', 'C3 선택', 'C2 선택', 'C4 선택', '창의 융합'],
 '2615': ['2학년 - 6', 'C2 선택', 'C3 선택', 'C1 선택', '창의 융합'],
 '3101': ['3-EF 수업반', '3-F 수업반', 'C3 선택', 'C2-CD 선택', 'C5 선택', 'C2-AB 선택'],
 '3102': ['3-AB 수업반', '3-ABE 수업반', '3-A 수업반', 'C4 선택', 'C1 선택', 'C2-AB 선택'],
 '3103': ['3-EF 수업반', '3-F 수업반', 'C3 선택', 'C4 선택', 'C2 선택'],
 '3104': ['3-CD 수업반', '3-D 수업반', 'C5 선택', 'C1 선택', 'C4 선택', 'C3-AB 선택'],
 '3105': ['3-CD 수업반', '3-D 수업반', 'C4 선택', 'C1-AB 선택', 'C3-AB 선택'],
 '3106': ['3-AB 수업반', '3-ABE 수업반', 'C3 선택', 'C5 선택', 'C1 선택', 'C4 선택'],
 '3107': ['3-CD 수업반', '3-D 수업반', 'C3 선택', 'C4 선택', 'C2 선택'],
 '3108': ['3-CD 수업반', '3-D 수업반', 'C3 선택', 'C5 선택', 'C2 선택', 'C4 선택'],
 '3109': ['3-CD 수업반', 'C1 선택', 'C2-CD 선택', '3-C 수업반', 'C5 선택', 'C3-CD 선택'],
 '3110': ['3-AB 수업반', '3-ABE 수업반', 'C1 선택', 'C5 선택', 'C2 선택', '3-B 수업반', 'C4 선택', 'C3-CD 선택'],
 '3111': ['3-AB 수업반', '3-ABE 수업반', '3-A 수업반', 'C4 선택', 'C2 선택', 'C1 선택'],
 '3112': ['3-AB 수업반', '3-ABE 수업반', 'C1 선택', 'C5 선택', 'C4 선택', 'C3 선택'],
 '3113': ['3-AB 수업반', '3-ABE 수업반', 'C2 선택', 'C5 선택', '3-B 수업반', 'C4 선택', 'C3 선택', 'C1-AB 선택'],
 '3114': ['3-AB 수업반', '3-ABE 수업반', '3-A 수업반', 'C3 선택', 'C4 선택', 'C1 선택'],
 '3115': ['3-CD 수업반', 'C3 선택', 'C2-CD 선택', '3-C 수업반', 'C5 선택'],
 '3116': ['3-EF 수업반', '3-F 수업반', 'C2 선택', 'C4 선택', 'C3 선택'],
 '3201': ['3-EF 수업반', '3-ABE 수업반', '3-E 수업반', 'C4 선택', 'C3 선택', 'C1-AB 선택', 'C2-AB 선택'],
 '3202': ['3-EF 수업반', '3-F 수업반', 'C4 선택', 'C2-CD 선택', 'C5 선택', 'C3 선택'],
 '3203': ['3-AB 수업반', '3-ABE 수업반', 'C2 선택', 'C4 선택', '3-B 수업반', 'C3 선택', 'C1-AB 선택'],
 '3204': ['3-AB 수업반', '3-ABE 수업반', '3-A 수업반', 'C4 선택', 'C1 선택'],
 '3205': ['3-EF 수업반', '3-F 수업반', 'C2 선택', 'C4 선택', 'C3 선택'],
 '3206': ['3-EF 수업반', '3-ABE 수업반', '3-E 수업반', 'C3 선택', 'C1 선택', 'C4 선택', 'C2-AB 선택'],
 '3207': ['3-AB 수업반', '3-ABE 수업반', '3-A 수업반', 'C3 선택', 'C1 선택'],
 '3208': ['3-CD 수업반', '3-D 수업반', 'C2-CD 선택', 'C4 선택', '창의 융합'],
 '3209': ['3-AB 수업반', '3-ABE 수업반', '3-A 수업반', 'C5 선택', 'C2 선택', 'C1 선택'],
 '3210': ['3-EF 수업반', '3-ABE 수업반', '3-E 수업반', 'C2 선택', 'C1 선택', 'C3 선택'],
 '3212': ['3-AB 수업반', '3-ABE 수업반', 'C1 선택', 'C5 선택', 'C2 선택', '3-B 수업반', 'C3 선택', 'C4 선택', '창의 융합'],
 '3213': ['3-AB 수업반', '3-ABE 수업반', '3-A 수업반', 'C3 선택', 'C1 선택', 'C4 선택', 'C2-AB 선택'],
 '3214': ['3-AB 수업반', '3-ABE 수업반', 'C3 선택', 'C4 선택', 'C2 선택', 'C5 선택', 'C1-AB 선택'],
 '3215': ['3-EF 수업반', '3-ABE 수업반', '3-E 수업반', 'C3 선택', 'C1-AB 선택', 'C2-AB 선택'],
 '3301': ['3-EF 수업반', '3-F 수업반', 'C3 선택', 'C2 선택'],
 '3302': ['3-AB 수업반',
  '3-ABE 수업반',
  'C1 선택',
  'C2-CD 선택',
  '3-B 수업반',
  'C3 선택',
  'C4 선택'],
 '3303': ['3-CD 수업반', '3-D 수업반', 'C4 선택', 'C1-AB 선택', 'C2 선택'],
 '3304': ['3-EF 수업반',
  '3-ABE 수업반',
  '3-E 수업반',
  'C3 선택',
  'C2-CD 선택',
  'C4 선택',
  'C1-AB 선택'],
 '3305': ['3-EF 수업반', '3-ABE 수업반', '3-E 수업반', 'C3 선택', 'C1 선택'],
 '3306': ['3-CD 수업반', '3-D 수업반', 'C2-CD 선택', 'C3-AB 선택', 'C4 선택'],
 '3307': ['3-EF 수업반',
  '3-ABE 수업반',
  '3-E 수업반',
  'C3 선택',
  'C5 선택',
  'C1 선택',
  'C4 선택'],
 '3308': ['3-AB 수업반', '3-ABE 수업반', '3-A 수업반', 'C2-CD 선택', 'C1 선택', 'C5 선택'],
 '3309': ['3-CD 수업반', '3-D 수업반', 'C4 선택', 'C2 선택', 'C1 선택', 'C3-CD 선택'],
 '3310': ['3-CD 수업반', 'C2 선택', 'C4 선택', '3-C 수업반', 'C1 선택', 'C3-CD 선택'],
 '3311': ['3-EF 수업반', '3-F 수업반', 'C3 선택', 'C2 선택'],
 '3312': ['3-AB 수업반', '3-ABE 수업반', '3-A 수업반', 'C3 선택', 'C4 선택', 'C1 선택'],
 '3313': ['3-EF 수업반', '3-ABE 수업반', '3-E 수업반', 'C1 선택', 'C4 선택', 'C3-AB 선택'],
 '3314': ['3-AB 수업반',
  '3-ABE 수업반',
  'C2 선택',
  'C3 선택',
  '3-B 수업반',
  'C5 선택',
  'C1 선택',
  'C4 선택'],
 '3315': ['3-EF 수업반',
  '3-F 수업반',
  'C4 선택',
  'C2-CD 선택',
  'C3 선택',
  'C5 선택',
  'C2-AB 선택',
  '창의 융합'],
 '3316': ['3-CD 수업반', 'C2 선택', 'C3 선택', '3-C 수업반', 'C5 선택', 'C4 선택'],
 '3401': ['3-CD 수업반', 'C2 선택', 'C4 선택', '3-C 수업반', 'C1 선택', 'C3-CD 선택'],
 '3402': ['3-CD 수업반', '3-D 수업반', 'C5 선택', 'C4 선택', 'C1-AB 선택'],
 '3403': ['3-CD 수업반', '3-D 수업반', 'C4 선택', 'C3 선택', 'C5 선택', 'C1-AB 선택'],
 '3404': ['3-AB 수업반', '3-ABE 수업반', '3-A 수업반', 'C4 선택', 'C2 선택', 'C5 선택'],
 '3405': ['3-EF 수업반', '3-F 수업반', 'C3 선택', 'C5 선택', 'C4 선택'],
 '3406': ['3-EF 수업반', '3-F 수업반', 'C2 선택', 'C5 선택', 'C4 선택'],
 '3407': ['3-EF 수업반', '3-ABE 수업반', '3-E 수업반', 'C1 선택', 'C2 선택', 'C4 선택', 'C3-AB 선택'],
 '3408': ['3-AB 수업반', '3-ABE 수업반', '3-A 수업반', 'C2-CD 선택', 'C1 선택', 'C4 선택'],
 '3409': ['3-EF 수업반', '3-F 수업반', 'C3 선택', 'C2 선택', 'C4 선택'],
 '3410': ['3-EF 수업반', '3-F 수업반', 'C4 선택', 'C5 선택', 'C3-AB 선택', '창의 융합'],
 '3411': ['3-CD 수업반', 'C4 선택', 'C2-CD 선택', '3-C 수업반', 'C1 선택', 'C3-CD 선택', 'C2-AB 선택'],
 '3412': ['3-EF 수업반',
  '3-ABE 수업반',
  '3-E 수업반',
  'C1 선택',
  'C2 선택',
  'C3 선택',
  'C4 선택'],
 '3413': ['3-CD 수업반', '3-D 수업반', 'C5 선택', 'C4 선택', 'C1-AB 선택'],
 '3414': ['3-CD 수업반',
  '3-D 수업반',
  'C2-CD 선택',
  'C4 선택',
  'C1 선택',
  'C5 선택',
  'C3 선택',
  '창의 융합'],
 '3415': ['3-AB 수업반',
  '3-ABE 수업반',
  'C1 선택',
  'C2-CD 선택',
  '3-B 수업반',
  'C3 선택',
  'C4 선택'],
 '3501': ['3-CD 수업반', 'C1 선택', 'C2-CD 선택', '3-C 수업반', 'C4 선택', 'C3-CD 선택'],
 '3502': ['3-CD 수업반', '3-D 수업반', 'C5 선택', 'C3-AB 선택'],
 '3503': ['3-EF 수업반', '3-ABE 수업반', '3-E 수업반', 'C2 선택', 'C1 선택'],
 '3504': ['3-EF 수업반', '3-F 수업반', 'C2 선택', 'C3 선택'],
 '3505': ['3-AB 수업반',
  '3-ABE 수업반',
  'C2 선택',
  'C3 선택',
  '3-B 수업반',
  'C5 선택',
  'C1 선택',
  'C4 선택'],
 '3506': ['3-AB 수업반',
  '3-ABE 수업반',
  'C1 선택',
  'C2-CD 선택',
  '3-B 수업반',
  'C5 선택',
  'C4 선택',
  'C3-CD 선택'],
 '3507': ['3-EF 수업반', '3-ABE 수업반', '3-E 수업반', 'C1 선택', 'C3-AB 선택'],
 '3508': ['3-EF 수업반',
  '3-ABE 수업반',
  '3-E 수업반',
  'C3 선택',
  'C1 선택',
  'C4 선택',
  'C2-AB 선택'],
 '3509': ['3-CD 수업반',
  '3-D 수업반',
  'C4 선택',
  'C5 선택',
  'C1 선택',
  'C3 선택',
  'C2-AB 선택'],
 '3510': ['3-CD 수업반',
  'C1 선택',
  'C5 선택',
  '3-C 수업반',
  'C4 선택',
  'C3 선택',
  'C2-AB 선택'],
 '3511': ['3-CD 수업반', '3-D 수업반', 'C3 선택', 'C1 선택', 'C4 선택'],
 '3512': ['3-EF 수업반', '3-ABE 수업반', '3-E 수업반', 'C3 선택', 'C2 선택', 'C1-AB 선택'],
 '3513': ['3-AB 수업반',
  '3-ABE 수업반',
  'C2 선택',
  'C4 선택',
  '3-B 수업반',
  'C1 선택',
  'C3-CD 선택'],
 '3514': ['3-AB 수업반',
  '3-ABE 수업반',
  'C1 선택',
  'C4 선택',
  '3-B 수업반',
  'C2 선택',
  'C3-AB 선택',
  'C5 선택',
  '창의 융합'],
 '3515': ['3-EF 수업반', '3-F 수업반', 'C2 선택', 'C3 선택', 'C4 선택'],
 '3516': ['3-CD 수업반', 'C1 선택', 'C2-CD 선택', '3-C 수업반', 'C3-CD 선택'],
 '3601': ['3-CD 수업반', 'C3 선택', 'C5 선택', '3-C 수업반', 'C1 선택'],
 '3602': ['3-AB 수업반', '3-ABE 수업반', '3-A 수업반', 'C3 선택', 'C2 선택', 'C1 선택'],
 '3603': ['3-CD 수업반', '3-D 수업반', 'C5 선택', 'C1 선택', 'C3-AB 선택'],
 '3604': ['3-CD 수업반', 'C4 선택', 'C2-CD 선택', '3-C 수업반', 'C1 선택', 'C3-CD 선택'],
 '3605': ['3-EF 수업반',
  '3-ABE 수업반',
  '3-E 수업반',
  'C1 선택',
  'C2 선택',
  'C5 선택',
  'C3-CD 선택',
  'C3-AB 선택'],
 '3606': ['3-AB 수업반', '3-ABE 수업반', '3-A 수업반', 'C3 선택', 'C4 선택', 'C1 선택'],
 '3607': ['3-AB 수업반', '3-ABE 수업반', '3-A 수업반', 'C3 선택', 'C1 선택', 'C2-AB 선택'],
 '3608': ['3-EF 수업반', '3-F 수업반', 'C2 선택', 'C4 선택', 'C5 선택'],
 '3609': ['3-EF 수업반', '3-F 수업반', 'C2 선택', 'C5 선택', 'C3 선택'],
 '3610': ['3-CD 수업반', 'C4 선택', 'C2-CD 선택', 'C5 선택', 'C3 선택', '3-C 수업반'],
 '3611': ['3-CD 수업반', 'C2 선택', 'C5 선택', '3-C 수업반', 'C1 선택', 'C3-CD 선택'],
 '3612': ['3-CD 수업반', 'C1 선택', 'C3 선택', '3-C 수업반', 'C2 선택', 'C4 선택'],
 '3613': ['3-AB 수업반',
  '3-ABE 수업반',
  'C3 선택',
  'C2-CD 선택',
  '3-B 수업반',
  'C5 선택',
  'C4 선택',
  'C1-AB 선택'],
 '3614': ['3-CD 수업반', 'C4 선택', 'C5 선택', 'C2 선택', '3-C 수업반', 'C1-AB 선택'],
 '3615': ['3-AB 수업반', '3-ABE 수업반', '3-A 수업반', 'C3 선택', 'C2 선택', 'C1 선택']}


st.header('시간표 확인')

# Streamlit 사이드바 입력
st.sidebar.header('2024.2학기 대구과학고')

# 학생 학번 입력
student_id = st.sidebar.text_input('학생 학번을 입력하세요')

# 날짜 입력 필드
today = datetime.today().strftime('%Y%m%d')
all_ti_ymd = st.sidebar.text_input('ALL_TI_YMD', value=today, placeholder=today)

# 학교코드 입력 필드
atpt_ofcdc_sc_code = st.sidebar.text_input('교육청코드', value='D10', placeholder='D10')
sd_schul_code = st.sidebar.text_input('학교번호', value='7240060', placeholder='7240060')

st.sidebar.text("학교 및 학기가 변경되면 학생의 강의실 정보를 수정해야 합니다.")

# 조회 버튼
if st.sidebar.button('시간표 조회'):
    # 학번으로 강의실 정보 찾기
    room_list = list(student_data[student_id])

    # NEIS API 요청
    def fetch_timetable(atpt_code, schul_code, date=None, room_list=None):
        api_key = 'f142b5caa822427392fb60899130ab0b'
        api_url = 'https://open.neis.go.kr/hub/hisTimetable'
        p_index = 1
        p_size = 100
        timetable_data = []

        while True:
            params = {
                'KEY': api_key,
                'ATPT_OFCDC_SC_CODE': atpt_code,
                'SD_SCHUL_CODE': schul_code,
                'Type': 'xml',
                'pIndex': p_index,
                'pSize': p_size
            }

            if date:
                params['ALL_TI_YMD'] = date

            response = requests.get(api_url, params=params, verify=False)
            response_content = response.content
            root = ET.fromstring(response_content)

            rows = root.findall('.//row')
            if not rows:
                break

            for row in rows:
                period = row.find('PERIO').text
                room_nm = row.find('CLRM_NM').text if row.find('CLRM_NM') is not None else '강의실 정보 없음'
                subject_nm = row.find('ITRT_CNTNT').text
                if room_nm in room_list:
                    timetable_data.append((period, room_nm, subject_nm))

            p_index += 1

        return timetable_data


    # 시간표 가져오기
    timetable = fetch_timetable(atpt_ofcdc_sc_code, sd_schul_code, all_ti_ymd, room_list)

    # DataFrame 생성
    df = pd.DataFrame(timetable, columns=['교시', '강의실', '과목'])

    # 교시별 데이터 병합
    df_grouped = df.groupby('교시')['과목'].apply(lambda x: ', '.join(x)).reset_index()

    # 시간표 출력
    st.subheader(f"{all_ti_ymd}일  {student_id} 학생의 시간표")
    st.dataframe(df_grouped)

else:
    st.info('학생 학번과 날짜를 입력하고 "시간표 조회" 버튼을 눌러주세요.')
