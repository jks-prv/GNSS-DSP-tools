# GPS L2CM code construction
#
# Copyright 2014 Peter Monta

import numpy as np

chip_rate = 511500
code_length = 10230

# initial-state table from pages 9--11 and pages 62--63 of IS-GPS-200H
# index is PRN

l2cm_init = {
    1: 0o742417664,    2: 0o756014035,    3: 0o002747144,    4: 0o066265724,
    5: 0o601403471,    6: 0o703232733,    7: 0o124510070,    8: 0o617316361,
    9: 0o047541621,   10: 0o733031046,   11: 0o713512145,   12: 0o024437606,
   13: 0o021264003,   14: 0o230655351,   15: 0o001314400,   16: 0o222021506,
   17: 0o540264026,   18: 0o205521705,   19: 0o064022144,   20: 0o120161274,
   21: 0o044023533,   22: 0o724744327,   23: 0o045743577,   24: 0o741201660,
   25: 0o700274134,   26: 0o010247261,   27: 0o713433445,   28: 0o737324162,
   29: 0o311627434,   30: 0o710452007,   31: 0o722462133,   32: 0o050172213,
   33: 0o500653703,   34: 0o755077436,   35: 0o136717361,   36: 0o756675453,
   37: 0o435506112,
   38: 0o771353753,   39: 0o226107701,   40: 0o022025110,   41: 0o402466344,
   42: 0o752566114,   43: 0o702011164,   44: 0o041216771,   45: 0o047457275,
   46: 0o266333164,   47: 0o713167356,   48: 0o060546335,   49: 0o355173035,
   50: 0o617201036,   51: 0o157465571,   52: 0o767360553,   53: 0o023127030,
   54: 0o431343777,   55: 0o747317317,   56: 0o045706125,   57: 0o002744276,
   58: 0o060036467,   59: 0o217744147,   60: 0o603340174,   61: 0o326616775,
   62: 0o063240065,   63: 0o111460621,
  159: 0o604055104,  160: 0o157065232,  161: 0o013305707,  162: 0o603552017,
  163: 0o230461355,  164: 0o603653437,  165: 0o652346475,  166: 0o743107103,
  167: 0o401521277,  168: 0o167335110,  169: 0o014013575,  170: 0o362051132,
  171: 0o617753265,  172: 0o216363634,  173: 0o755561123,  174: 0o365304033,
  175: 0o625025543,  176: 0o054420334,  177: 0o415473671,  178: 0o662364360,
  179: 0o373446602,  180: 0o417564100,  181: 0o000526452,  182: 0o226631300,
  183: 0o113752074,  184: 0o706134401,  185: 0o041352546,  186: 0o664630154,
  187: 0o276524255,  188: 0o714720530,  189: 0o714051771,  190: 0o044526647,
  191: 0o207164322,  192: 0o262120161,  193: 0o204244652,  194: 0o202133131,
  195: 0o714351204,  196: 0o657127260,  197: 0o130567507,  198: 0o670517677,
  199: 0o607275514,  200: 0o045413633,  201: 0o212645405,  202: 0o613700455,
  203: 0o706202440,  204: 0o705056276,  205: 0o020373522,  206: 0o746013617,
  207: 0o132720621,  208: 0o434015513,  209: 0o566721727,  210: 0o140633660
}

def l2cm_shift(x):
  return (x>>1) ^ (x&1)*0o445112474;

def make_l2cm(prn):
  x = l2cm_init[prn]
  n = code_length
  y = numpy.zeros(n)
  for i in range(n):
    y[i] = x&1
    x = l2cm_shift(x)
  return y

codes = {}

def l2cm_code(prn):
  if not codes.has_key(prn):
    codes[prn] = make_l2cm(prn)
  return codes[prn]

def code(prn,chips,frac,incr,n):
  c = l2cm_code(prn)
  idx = (chips%code_length) + frac + incr*np.arange(n)
  idx = np.floor(idx).astype('int')
  idx = np.mod(idx,code_length)
  x = c[idx]
  return 1.0 - 2.0*x

# test vectors in IS-GPS-200H

l2cm_end_state = {
    1: 0o552566002,    2: 0o034445034,    3: 0o723443711,    4: 0o511222013,
    5: 0o463055213,    6: 0o667044524,    7: 0o652322653,    8: 0o505703344,
    9: 0o520302775,   10: 0o244205506,   11: 0o236174002,   12: 0o654305531,
   13: 0o435070571,   14: 0o630431251,   15: 0o234043417,   16: 0o535540745,
   17: 0o043056734,   18: 0o731304103,   19: 0o412120105,   20: 0o365636111,
   21: 0o143324657,   22: 0o110766462,   23: 0o602405203,   24: 0o177735650,
   25: 0o630177560,   26: 0o653467107,   27: 0o406576630,   28: 0o221777100,
   29: 0o773266673,   30: 0o100010710,   31: 0o431037132,   32: 0o624127475,
   33: 0o154624012,   34: 0o275636742,   35: 0o644341556,   36: 0o514260662,
   37: 0o133501670,
   38: 0o453413162,   39: 0o637760505,   40: 0o612775765,   41: 0o136315217,
   42: 0o264252240,   43: 0o113027466,   44: 0o774524245,   45: 0o161633757,
   46: 0o603442167,   47: 0o213146546,   48: 0o721323277,   49: 0o207073253,
   50: 0o130632332,   51: 0o606370621,   52: 0o330610170,   53: 0o744312067,
   54: 0o154235152,   55: 0o525024652,   56: 0o535207413,   57: 0o655375733,
   58: 0o316666241,   59: 0o525453337,   60: 0o114323414,   61: 0o755234667,
   62: 0o526032633,   63: 0o602375063,
  159: 0o425373114,  160: 0o427153064,  161: 0o310366577,  162: 0o623710414,
  163: 0o252761705,  164: 0o050174703,  165: 0o050301454,  166: 0o416652040,
  167: 0o050301251,  168: 0o744136527,  169: 0o633772375,  170: 0o007131446,
  171: 0o142007172,  172: 0o655543571,  173: 0o031272346,  174: 0o203260313,
  175: 0o226613112,  176: 0o736560607,  177: 0o011741374,  178: 0o765056120,
  179: 0o262725266,  180: 0o013051476,  181: 0o144541215,  182: 0o534125243,
  183: 0o250001521,  184: 0o276000566,  185: 0o447447071,  186: 0o000202044,
  187: 0o751430577,  188: 0o136741270,  189: 0o257252440,  190: 0o757666513,
  191: 0o606512137,  192: 0o734247645,  193: 0o415505547,  194: 0o705146647,
  195: 0o006215430,  196: 0o371216176,  197: 0o645502771,  198: 0o455175106,
  199: 0o127161032,  200: 0o470332401,  201: 0o252026355,  202: 0o113771472,
  203: 0o754447142,  204: 0o627405712,  205: 0o325721745,  206: 0o056714616,
  207: 0o706035241,  208: 0o173076740,  209: 0o145721746,  210: 0o465052527
}

def test_end_state(prn):
  x = l2cm_init[prn]
  n = code_length
  for i in range(n-1):
    x = l2cm_shift(x)
  return x

if __name__=='__main__':
  for prn in l2cm_end_state.keys():
    s = test_end_state(prn)
    t = l2cm_end_state[prn]
    if s!=t:
      print "prn %d: ***mismatch*** %09o %09o" % (prn,s,t)
    else:
#      print "prn %d: %09o %09o" % (prn,s,t)
      pass
