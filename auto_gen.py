# -*- coding: UTF-8 -*-
import sys, getopt, os, datetime,requests
from os.path import expanduser

def handle_dates(arg, due_dater):
    cur_time = datetime.datetime.today()
    if (arg[0] == '!') :
        due_dater = arg[1:] + due_dater
    elif ('+' in arg) or ('-' in arg) :
        try:
            ch = '+' if '+' in arg else '-'
            symb = 1 if ch == '+' else -1
            lstr,rstr = map(str.strip, arg.strip().split(ch))
            print(lstr)
            base = get_date(lstr)
            delta = datetime.timedelta(days=(int(rstr) * symb))
            base += delta
            due_dater = to_time_str(base)
        except EOFError:
            print("!")
            sys.exit(2)
    elif (arg in ("t","to","today","tomorrow","yesterday","y")) : 
        due_dater = to_time_str(get_date(arg))
    elif (len(arg) == 8 and str.isdigit(arg)) :
        due_dater = str(int(arg[0 : 4])) +" \\ 年 \\ " + str(int(arg[4 : 6])) + " \\ 月 \\ " + str(int(arg[6 : 8])) + " \\ 日 " + due_dater
    print(due_dater)
    return due_dater

def init_conf(path):
    author_idl = "\\newcommand{\\hmwkAuthorID}{"
    author_classl = "\\newcommand{\\hmwkAuthorClass}{"
    author_namel = "\\newcommand{\\hmwkAuthorName}{"
    print("您的姓名?")
    author_namer = input() + "}"
    print("您的学号?")
    author_idr = input() + "}"
    print("您所在的班级?")
    author_classr = input() + "}"
    with open(path, 'w', encoding='utf-8') as fi:
        fi.write(author_classl + author_classr + '\n')
        fi.write(author_idl + author_idr + '\n')
        fi.write(author_namel + author_namer + '\n')

def to_time_str(date):
    yy,mmmm,dd = str.split(date.isoformat(), '-')
    print(yy + mmmm + dd)
    due_dater = str(int(yy)) + " \\ 年 \\ " + str(int(mmmm)) + " \\ 月 \\ " + str(int(dd[0:2])) + " \\ 日 " + "}"
    return due_dater

def get_date(val) :
    if (val == 'today' or val == 't') :
        return datetime.datetime.today()
    elif (val == 'tomorrow' or val == 'to'):
        return datetime.datetime.today() + datetime.timedelta(days = 1)
    elif (val == 'yesterday' or val == 'y'):
        return datetime.datetime.today() + datetime.timedelta(days = -1)
    else :
        assert(len(val) == 8)
        return datetime.datetime.fromisoformat(val[0 : 4] + '-' + val[4 : 6] + '-' + val[6 : 8])
def main(argv):
    titlel = "\\newcommand{\\hmwkTitle}{"
    titler = "}"
    due_datel = "\\newcommand{\\hmwkDueDate}{"
    due_dater = "}"
    class_namel = "\\newcommand{\\hmwkClass}{"
    class_namer = "}"
    class_timel = "\\newcommand{\\hmwkClassTime}{}"
    instructorl = "\\newcommand{\\hmwkClassInstructor}{}"
    chk_len_ins = len(instructorl)
    chk_len_ct = len(class_timel)
    finish_time = "\\date{"
    hp = '''
文档生成器,用于生成填好个人信息的文档
会自动在用户目录下生成一个"auto_gen_latex.ini"文件, 用于保存学号, 姓名和班级
参数:
-h, --help 显示帮助 
-t, --title= 作业标题, 会自动在以这个为标题的目录下生成文件
-s, --sub= 科目,不加这个参数的话默认获取当前工作目录的名字
-f, --finish-time 署名下的日期,一般是完成日期, 默认生成为今天, 
           可以使用today(也可写成t), tomorrow(也可写成to), yesterday(也可写成y), yyyyMMdd,
           如果想表示相对时间, 如today+2表示后天,today-1, 表示昨天(不支持乘除操作).
           其他情况先输入!再输入自定义的时间如!1145141919, 会在文档中原样显示 
-d, --due= 截止时间, 可以使用today(也可写成t), tomorrow(也可写成to), yesterday(也可写成y), yyyyMMdd,
           如果想表示相对时间, 如today+2表示后天,today-1, 表示昨天(不支持乘除操作).
           其他情况先输入!再输入自定义的时间如!1145141919, 会在文档中原样显示
-s, -d是必选参数
-i, --instructor 教师姓名(可选, 需要与-c一同使用)
-c, --class-time 上课时间(可选, 需要与-i一同使用)
-r, --reset 重置写入到auto_gen_latex.ini文件的配置信息
--no-test-run 生成之后不测试编译
'''
    test_run_flg = True
    try:
        opts, args = getopt.getopt(argv,"ht:s:d:r:i:c:f:",["title=","sub=","due=","help","reset","no-test-run","instructor","class-time","finish-time"])
    except getopt.GetoptError:
        print(hp)
        sys.exit(2)
    if len(opts) == 0 :
        print(hp)
        sys.exit()
    file_path = expanduser("~") + "\\auto_gen_latex.ini"
    for opt, arg in opts:
        if opt in ("-i", "--instructor") :
            instructorl = instructorl[:len(instructorl) - 1] + arg + "}"
        elif opt in ("-c", "--class-time") :
            class_timel = class_timel[:len(class_timel) - 1] + arg + "}"
        elif opt == "--no-test-run":
            test_run_flg = False
        elif opt in ('-h',"--help"):
            print(hp)
            sys.exit()
        elif opt in ("-t", "--title"):
            titler = arg + titler
            print(titler)
        elif opt in ("-s", "--sub"):
            class_namer = arg + class_namer
            print(class_namer)
        elif opt in ("-f","--finish-time") :
            finish_time = finish_time + handle_dates(arg, "}")
        elif opt in ("-d","--due"):
            due_dater = handle_dates(arg, due_dater)
        elif opt in ("-r", "--reset"):
            init_conf(file_path)
            sys.exit()
        else :    
            print(opt)
            sys.exit(2)
    if (os.path.exists(file_path) == False) :
        print("配置文件不存在!, 要现在初始化吗?(Y/N)")
        option = input()
        while option not in ("Y","N","Yes","No") :
            print("配置文件不存在!, 要现在初始化吗?(Y/N)")
            option = input()
            if (option in ("Y", "Yes")) :
                init_conf(file_path)
                break
    if (class_namer == '}') :
        dir = os.getcwd().split("\\")[-1]
        class_namer = dir + class_namer
    if (titler[0] == '}' or class_namer =='}' or due_dater == '}') :
        print("-t, -s, -d 必须给出, 请检查")
        sys.exit(2)
    if ((len(instructorl) == chk_len_ins) ^ (chk_len_ct == len(class_timel))) :
        print("-i, -c 必须同时给出, 请检查")
        sys.exit(2)
    # 开始整活
    os.mkdir(titler[:len(titler) - 1])
    hm_url = "https://raw.githubusercontent.com/solidhtwoo/latex-homework-template-chinese/master/homework.tex"
    os.chdir(titler[:len(titler) - 1])
    with open("homework.tex","w", encoding='utf-8') as hm :
        tmp = requests.get(hm_url)
        tmp.encoding = 'utf-8'
        hm.write(tmp.text)
    if (finish_time == "\\date{") :
        finish_time = "\\date{\\today}"
    with open(file_path, 'r', encoding='utf-8') as fi:
        with open("info.tex", 'w', encoding='utf-8') as fo:
            for ln in fi.readlines():
                fo.write(ln + '\n')
            fo.write(titlel + titler + '\n')
            fo.write(class_namel + class_namer + '\n')
            fo.write(due_datel + due_dater + '\n')
            fo.write(instructorl + "\n")
            fo.write(class_timel + '\n')
            fo.write(finish_time + "\n")
    if(test_run_flg) :
        print(os.system("latexmk -xelatex -latexoption=-file-line-error -latexoption=-interaction=nonstopmode -latexoption=-shell-escape homework.tex"))
if __name__ == "__main__":
   main(sys.argv[1:])
