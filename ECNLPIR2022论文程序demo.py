#import pycantonese
#url = ("https://childes.talkbank.org/data/Biling/YipMatthews.zip")
#corpus = pycantonese.read_chat(url)
#corpus.n_files()
#len(corpus.words())

#corpus = pycantonese.hkcancor()
#corpus.head()

import os
import pycantonese
import json
#import jieba
from graphviz import Digraph
from pyltp import  Postagger, NamedEntityRecognizer, Parser,SementicRoleLabeller
import zhconv
def addwords(word,attr):#将某个特定粤语词语加入FC-RPlus_v.cha文件
    word= zhconv.convert(word.strip(), 'zh-hk')
    #word=word.strip()
    path=pycantonese.__file__
    (filepath, tempfilename) = os.path.split(path)
    filepath=filepath+'\\data\\hkcancor\\FC-RPlus_v.cha'
    #print(filepath)
    f = open(filepath,'r+',encoding="utf-8")
    f_line_xxa=f.readline()
    f_lines_a=f_line_xxa.split('\t')
    f_line_mor=f.readline()
    f_lines_m=f_line_mor.split('\t')
    
    wordin=word in f_lines_a
    if not wordin:
        f_line_xxa=f_lines_a[0]+'\t'+word
        for i in range(1,len(f_lines_a)):
            f_line_xxa=f_line_xxa+'\t'+f_lines_a[i]
        f_line_mor=f_lines_m[0]+'\t'+attr
        for i in range(1,len(f_lines_m)):
            f_line_mor=f_line_mor+'\t'+f_lines_m[i]
        
        f.seek(0,0)
        f.write(f_line_xxa)
        f.write(f_line_mor)
        f.close()
def CanToMan(words):#找出粤语词汇对应的国语词汇，这里没用上
    
    path=pycantonese.__file__
    (filepath, tempfilename) = os.path.split(path)
    filepath=filepath+'\\data\\can_man\\hkcandict.json'
    
    f =open(filepath,encoding='utf-8') #打开‘hkcandict.json’的json文件
    res=f.read()  #读文件
    hkcandict=json.loads(res)#把json串变成python的数据类型：字典
    tmwords=[]
    for i in range(len(words)):
        if words[i] in hkcandict:#[words[i]]["Mor"][0]["国语释义"]:
            tmwords.append(hkcandict[words[i]]["Mor"][0]["国语释义"])
        elif words[i]:
            tmwords.append(words[i])
        
    f.close()
    return tmwords
def update_POSword(word):#更新词语词性
    
    path=pycantonese.__file__
    (filepath, tempfilename) = os.path.split(path)
    filepath=filepath+'\\pos_tagging\\POS_dict.json'
    #print(filepath)
    f =open(filepath,encoding='utf-8') #打开‘cce-cedict.json’的json文件
    res=f.read()  #读文件
    POSdict=json.loads(res)#把json串变成python的数据类型：字典
    if POSdict[word]["POS"]:
        f.close()
        return POSdict[word]["POS"]
    else:
        return "X"
    f.close()
if __name__=='__main__':
#    data="我都系，我叫李明。好高兴识得你。"
    data="张女士哋我妈咪嘅好朋友,佢系做惯乞儿懒做官。"
    data="話就話係公平競爭，到最後咪又係塘水滾塘魚。"
    data="佢哋两个大缆都扯唔埋，你能撮合到佢哋，我㓟个头畀你当凳坐。"
    
    hkdata= zhconv.convert(data, 'zh-hk')#将简体字粤语句子转成繁体字粤语句子
    
   
    addwords(' 大缆都扯唔埋','a|daai6laam6dou1ce2m4maai4')
    addwords(' 㓟个头畀你当凳坐','v|pai1go3tau4bei2nei5dong3dang3tso5')
    addwords(' 一戙都冇','a|jat7dung6dou1mou5')
    addwords(' 一頭霧水','a|jat7tau4mou6soey2')
    addwords(' 呢排','adv|ni1paai4')
    
    corpus=pycantonese.parse_text(hkdata)#调用pycantonese分析处理粤语句子hkdata，结果给corpus对象
    #tmp=corpus.head()
    #print(tmp)
    words=corpus.words()#将corpus对象里分词好的粤语词汇列表保存到words列表
    for i in range(len(words)):#将繁体字粤语词汇转成简体字粤语词汇
        words[i]=zhconv.convert(words[i], 'zh2Hans')
    #print(words)
    token_list=corpus.tokens()#将corpus对象里列表列表保存到token_list列表
    #以下是每个节点信息的含义
    #word='佢哋', Word form of the token，令牌标志的单词形式，即分析研究的粤语词汇
    #pos='PRON',Part-of-speech tag,该粤语词汇的词性
    #jyutping='keoi5dei6',Jyutping romanization,粤语拼音的罗马表示，即该粤语词汇的粤语拼音
    #mor='he',Morphological information，词法信息，这里是该粤语词汇的英文
    #gloss='he',其实是Gloss in English，该粤语词汇的英文
    #gra=None, gra 表示Grammatical relation，即语法关系项，这个属性只针对英语，所以一般是none
    for i in range(len(token_list)):#打印token_list以便查看的结果
        print(token_list[i])
    

    
    # 词性标注
    

    postags = [token_list[i].pos for i in range(len(words))]#根据Pycantonese获取的token_list列表里每个词语的词性构造词性列表用于pyltp的句法分析输入
    
    
    # 依存句法分析
    
    par_model_path = os.path.join(os.path.dirname(__file__), 'ltp_data_v3.4.0/parser.model')
    mparser = Parser()
    mparser.load(par_model_path)
    tmpwords=words
    arcs = mparser.parse(words, postags)
    mparser.release()
    #print(type(arcs))
    rely_id = [arc.head for arc in arcs]  # 提取依存父节点id
    relation = [arc.relation for arc in arcs]  # 提取依存关系
    print(relation)
    heads = ['Root' if id == 0 else words[id-1] for id in rely_id]  # 匹配依存父节点词语
    headns = ['Root' if id == 0 else 'cyw'+str(id-1) for id in rely_id]  # 匹配依存父节点词语

    g2 = Digraph('cxpy')
    c0 = Digraph(name='child0')#粤语词汇结点
    c0.graph_attr['rankdir'] = 'LR'
    c1 = Digraph(name='child2', node_attr={'shape': 'plaintext'})#粤语词汇的粤语拼音结点
    c1.graph_attr['rankdir'] = 'LR'
    c3 = Digraph(name='child3', node_attr={'shape': 'plaintext'})#粤语词汇的词性结点
    c3.graph_attr['rankdir'] = 'LR'
    '''
    新細明體：PMingLiU
    細明體：MingLiU
    標楷體：DFKai-SB
    黑体：SimHei
    宋体：SimSun
    新宋体：NSimSun
    仿宋：FangSong
    楷体：KaiTi
    仿宋_GB2312：FangSong_GB2312
    楷体_GB2312：KaiTi_GB2312
    微軟正黑體：Microsoft JhengHei
    微软雅黑体：Microsoft YaHei
    '''
    
    #mwords=['他', '今天', '写', '那些', '东西', '，', '什么东西', '都', '八竿子打不着', '。']
    #mwords=CanToMan(words)
    
    #print(mwords)
    
    for i in range(len(words)):
        words[i]=zhconv.convert(words[i], 'zh2Hans')#简体字转成繁体字        
        c0.node(name='cy'+str(i),fontname="Microsoft JhengHei",label=words[i])#构造粤语词汇的结点
    for i in range(len(words)):
        if token_list[i].jyutping:
            c1.node(name='cj'+str(i),fontname="Microsoft YaHei",label=token_list[i].  jyutping)#构造粤语词汇对应粤语拼音的结点
        else:
            c1.node(name='cj'+str(i),fontname="Microsoft YaHei",label='')
    for i in range(len(words)):
        c3.node(name='cx'+str(i),fontname="Microsoft YaHei",label=token_list[i].pos)#构造粤语词汇对应词性的结点

    #将粤语词汇，粤语词汇的粤语拼音，粤语词汇的词性三个子图放到g2图中
    g2.subgraph(c0)
    g2.subgraph(c1)
    g2.subgraph(c3)
    
    for i in range(len(words)):
        g2.edge('cy'+str(i), 'cj'+str(i),style="invis",len='0.1')#词语结点连线到对应词语的粤语拼音结点，因style为不可见，其实是为了对齐这些结点
        g2.edge('cj'+str(i), 'cx'+str(i),style="invis",len='0.1')#粤语拼音结点连线到对应词语的词性结点，因style为不可见，其实是为了对齐这些结点
        
        
    
    g = Digraph('jffx')
    g.attr(rankdir="same" )
    for i in range(len(words)):
    #g.node(name=word,fontname="Microsoft YaHei")
        g.node(name='cyw'+str(i),fontname="Microsoft YaHei",label=words[i])#构造粤语词汇的结点
    
    g.node(name='Root', fontname="Microsoft YaHei")#根节点
    for i in range(len(words)):#标出粤语词汇之间的依存关系
        if relation[i] not in ['HED']:
            g.edge(headns[i],'cyw'+str(i),label=relation[i])
        else:
            if heads[i] == 'Root':
                g.edge('Root', 'cyw'+str(i), label=relation[i])
            else:
                g.edge('Root',headns[i],  label=relation[i])
    #print(g.source)
    #g.view()

    g2.render('cxpy.gv', view=False)#根据cxpy.gv形成pdf文件但不打开
    
    g.render('jffx.gv', view=False)#根据jffx.gv形成pdf文件但不打开
    
    import shutil
    if os.path.isfile("Sample1.pdf"):
        os.unlink("Sample1.pdf")
    if os.path.isfile("Sample2.pdf"):
        os.unlink("Sample2.pdf")
    shutil.copy("cxpy.gv.pdf","Sample1.pdf")
    shutil.copy("jffx.gv.pdf","Sample2.pdf")

    from PyPDF2 import PdfWriter, PdfReader, PageObject,Transformation

    pdf_filenames = ['Sample1.pdf','Sample2.pdf','Sample3.pdf']
    inputpdf1 = PdfReader(open(pdf_filenames[0], 'rb'), strict=False)
    inputpdf2 = PdfReader(open(pdf_filenames[1], 'rb'), strict=False)

    page1 = inputpdf1.pages[0]
    page2 = inputpdf2.pages[0]

    pdf_writer = PdfWriter()

    total_width = max([page1.mediabox.upper_right[0], page2.mediabox.upper_right[0]])
    total_height =page1.mediabox.upper_right[1] + page2.mediabox.upper_right[1]
    new_page = PageObject.create_blank_page(None, total_width, total_height)

    #page2.merge_page(page1)
    page1.add_transformation(Transformation().translate((total_width-page1.mediabox.upper_right[0])/2,page2.mediabox.upper_right[0]-150),1);
    page2.add_transformation(Transformation().translate((total_width-page2.mediabox.upper_right[0])/2,0),1);
    new_page.merge_page(page1,0)
    new_page.merge_page(page2,0)
    pdf_writer.add_page(new_page)
    with open('MergedPDF.pdf','wb') as fileobj:
        pdf_writer.write(fileobj)
    os.startfile('MergedPDF.pdf')

    
