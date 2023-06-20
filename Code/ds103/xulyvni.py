def xuly_vni(df):
        from pandas_profiling import ProfileReport
        from underthesea import word_tokenize, pos_tag, sent_tokenize
        import regex
        import demoji
        ##LOAD EMOJI ICON
        file = open('files/emojicon.txt', 'r', encoding="utf8")
        emoji_lst = file.read().split('\n')
        emoji_dict = {}
        for line in emoji_lst:
                key, value = line.split('\t')
                emoji_dict[key] = str(value)
        file.close()
        #LOAD TEENCODE
        file = open('files/teencode.txt', 'r', encoding="utf8")
        teen_lst = file.read().split('\n')
        teen_dict = {}
        for line in teen_lst:
            key, value = line.split('\t')
            teen_dict[key] = str(value)
        file.close()
        #LOAD TRANSLATE ENGLISH TO VIETNAMESE
        file = open('files/englishtovietnamese.txt', 'r', encoding="utf8")
        english_lst = file.read().split('\n')
        english_dict = {}
        for line in english_lst:
            key, value = line.split('\t')
            english_dict[key] = str(value)
        file.close()
        #LOAD WRONG WORDS
        file = open('files/wrong-word.txt', 'r', encoding="utf8")
        wrong_lst = file.read().split('\n')
        file.close()
        #LOAD STOPWORDS
        file = open('files/vietnamese-stopwords.txt', 'r', encoding="utf8")
        stopwords_lst = file.read().split('\n')
        file.close()

        def process_text(text, emoji_dict, teen_dict, wrong_lst):
            document = text.lower()
            document = document.replace("'",'')
            document = regex.sub(r'\.+', ".", document)
            new_sentence =''
            for sentence in sent_tokenize(document):
                # if not(sentence.isascii()):
                ###### CONVERT EMOJICON
                sentence = ''.join(emoji_dict[word] + ' ' if word in emoji_dict else word for word in list(sentence))
                ###### CONVERT TEENCODE
                sentence = ' '.join(teen_dict[word] if word in teen_dict else word for word in sentence.split())
                ###### REMOVE PUNCTUATIONS AND NUMBERS
                pattern = r'(?i)\b[a-záàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđ]+\b'
                sentence = ' '.join(regex.findall(pattern,sentence))
                ###### REMOVE WRONG WORDS 
                sentence = ' '.join('' if word in wrong_lst else word for word in sentence.split())
                new_sentence = new_sentence+ sentence + '. '                    
            document = new_sentence  
            ###### REMOVE EXCESS BLANK SPACE
            document = regex.sub(r'\s+', ' ', document).strip()
            return document
        df['processed_text'] = df['comment'].apply(lambda x: process_text(x, emoji_dict, teen_dict, wrong_lst))

        # REMOVE HTTPS LINKS
        df['processed_text'] = df['processed_text'].replace(
        r'((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*', '',
        regex=True)
        
        # UNICODE NORMALIZATION
        def loaddicchar():
            uniChars = "àáảãạâầấẩẫậăằắẳẵặèéẻẽẹêềếểễệđìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵÀÁẢÃẠÂẦẤẨẪẬĂẰẮẲẴẶÈÉẺẼẸÊỀẾỂỄỆĐÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴÂĂĐÔƠƯ"
            unsignChars = "aaaaaaaaaaaaaaaaaeeeeeeeeeeediiiiiooooooooooooooooouuuuuuuuuuuyyyyyAAAAAAAAAAAAAAAAAEEEEEEEEEEEDIIIOOOOOOOOOOOOOOOOOOOUUUUUUUUUUUYYYYYAADOOU"

            dic = {}
            char1252 = 'à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ'.split(
                '|')
            charutf8 = "à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ".split(
                '|')
            for i in range(len(char1252)):
                dic[char1252[i]] = charutf8[i]
            return dic
         
        def covert_unicode(txt):
            dicchar = loaddicchar()
            return regex.sub(
                r'à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ',
                lambda x: dicchar[x.group()], txt)
                
        df['processed_text'] = df['processed_text'].apply(lambda x: covert_unicode(x))
        # SPECIAL WORDS
        def process_special_word(text):
            new_text = ''
            text_lst = text.split()
            i= 0
            if 'không' in text_lst or 'rất' in text_lst or 'quá' in text_lst or 'gần' in text_lst or 'sai' in text_lst or 'bị' in text_lst or 'như' in text_lst or 'cũng' in text_lst or 'hơi' in text_lst:
                while i <= len(text_lst) - 1:
                    word = text_lst[i]
                    if  word in ['không','rất','quá','gần','sai','bị','như','y','cũng','hơi']:
                        next_idx = i+1
                        if next_idx <= len(text_lst) -1:
                            word = ' ' + word +'_'+ text_lst[next_idx]
                        i= next_idx + 1
                    else:
                        i = i+1
                    new_text = new_text + word + ' '
            else:
                new_text = text
            return new_text.strip()
        
        df['processed_text'] = df['processed_text'].apply(lambda x: process_special_word(x))
                
        # POS-TAG
        def process_postag_thesea(text):
            new_document = ''
            for sentence in sent_tokenize(text):
                sentence = sentence.replace('.','')
                lst_word_type = ['N','Np','A','AB','V','VB','VY','R']
                sentence = ' '.join( word[0] if word[1].upper() in lst_word_type else '' for word in pos_tag(process_special_word(word_tokenize(sentence, format="text"))))
                new_document = new_document + sentence + ' '
            new_document = regex.sub(r'\s+', ' ', new_document).strip()
            return new_document
        df['processed_text'] = df['processed_text'].apply(lambda x: process_postag_thesea(x))
        

        # REMOVE STOP WORDS
        def remove_stopword(text, stopwords):
            document = ' '.join('' if word in stopwords else word for word in text.split())
            document = regex.sub(r'\s+', ' ', document).strip()
            return document
        df['processed_text'] = df['processed_text'].apply(lambda x: remove_stopword(x,stopwords_lst))
 
        return df
