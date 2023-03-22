def hospitalProc(filename):
    
    with open(filename,'r',encoding='utf-8') as f:
        data = f.read().splitlines()
    hospitals = [i.split('\t') for i in data]
    with open('reshost.txt','w',encoding='utf-8') as fw:
        for item in hospitals:
            name = item[1]
            location = item[2].split('、')[0].split('，')[0].split('/')[0].split('；')[0]
            district = item[3]
            level = 5 if item[6] =='甲' else 4
            fw.writelines(name+'\t'+location+'\t'+district+'\t'+str(level)+'\n')
        
        
        
        
hospitalProc('hospital2.txt')