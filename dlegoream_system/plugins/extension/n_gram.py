def ngram(text: str, n: int):
       
        if n <= 0:
            return []
        if n > len(text):
            return []
            
        ngram_list =[text[i:i+n] for i in range(len(text) - n + 1)]

        return ngram_list