# 运行方式
# ./run.sh commands test_command
ngramsymbols < $1.txt > $1.syms # 从文本里生成所有可能的词 以空格作为分隔符
farcompilestrings -symbols=$1.syms -keep_symbols=1 $1.txt > $1.far # 把所有词转换成对应编号
ngramcount $1.far > $1.cnts # 输出所有的n-gram数量
ngrammake $1.cnts > $1.mod # 计算n-gram模型
ngramrandgen $1.mod | farprintstrings # 打印n-gram模型
fstcompile --isymbols=commands.syms --osymbols=commands.syms $2.txt > $2.fst # 编译fst
fstcompose $2.fst commands.mod | fstshortestpath | fstproject --project_output | fstrmepsilon | fsttopsort | fstprint --isymbols=commands.syms --osymbols=commands.syms # 找到最大概率的序列


