#!/usr/bin/python
#-*- coding:utf-8 -*-

FGRi_conc_txt = """12.47
18.68
24.88
31.06
37.22
43.37
49.5
55.62
61.73
73.89
79.95
86
98.04
104.04
110.02
116
121.95
133.82
139.73
145.63
169.08
192.31
198.08
203.84
226.73
238.1
243.76
249.41
255.04
260.66
271.87
277.45
283.02
305.16
327.1
332.56
338
348.84
354.24
359.63
365.01
370.37
381.06
386.39
391.71
412.84
433.79
439
444.19
454.55
459.7
464.85
485.33
505.62"""


init_design_txt = """Dish_No	well_no	細胞剥離方法	trypsin_time	FGRi濃度	preconditioning_period	suspend速度	KSR期間	3因子期間
1	1	single	3	100	1	10	3	7
1	2	single	8	100	1	20	8	19
1	3	single	13	100	3	10	13	11
1	4	single	18	100	6	100	8	11
1	5	single	23	100	3	100	3	19
1	6	single	28	100	6	20	13	7
2	1	single	3	200	3	20	8	11
2	2	single	8	200	3	100	13	7
2	3	single	13	200	6	20	3	19
2	4	single	18	200	1	10	13	19
2	5	single	23	200	6	10	8	7
2	6	single	28	200	1	100	3	11
3	1	single	3	500	6	100	13	19
3	2	single	8	500	6	10	3	11
3	3	single	13	500	1	100	8	7
3	4	single	18	500	3	20	3	7
3	5	single	23	500	1	20	13	11
3	6	single	28	500	3	10	8	19
4	1	single	3	100	6	10	3	11
4	2	single	8	200	6	10	8	11
4	3	single	13	0	0	10	8	11
4	4	single	18	100	6	10	8	11
4	5	single	23	500	1	10	8	11
4	6	single	28	100	6	10	8	19
5	1	double	3	100	1	10	3	7
5	2	double	8	100	1	20	8	19
5	3	double	13	100	3	10	13	11
5	4	double	18	100	6	100	8	11
5	5	double	23	100	3	100	3	19
5	6	double	28	100	6	20	13	7
6	1	double	3	200	3	20	8	11
6	2	double	8	200	3	100	13	7
6	3	double	13	200	6	20	3	19
6	4	double	18	200	1	10	13	19
6	5	double	23	200	6	10	8	7
6	6	double	28	200	1	100	3	11
7	1	double	3	500	6	100	13	19
7	2	double	8	500	6	10	3	11
7	3	double	13	500	1	100	8	7
7	4	double	18	500	3	20	3	7
7	5	double	23	500	1	20	13	11
7	6	double	28	500	3	10	8	19
8	1	double	3	100	6	10	3	11
8	2	double	8	200	6	10	8	11
8	3	double	13	0	0	10	8	11
8	4	double	18	100	6	10	8	11
8	5	double	23	500	1	10	8	11
8	6	double	28	100	6	10	8	19

"""
init_design_txt = init_design_txt.replace("single", "0").replace("double", "1")

