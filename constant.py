#coding:utf-8

class Region:
    CN = 1
    HK = 2
    US = 3

class ChinaTag:
    @staticmethod
    def is_sh(code):
        return code.startswith("60")
    
    @staticmethod
    def is_sz(code):
        return code[:2] in ('00', '30')
    
    @staticmethod
    def get(code):
        if ChinaTag.is_sh(code):
            return 'ss'
        
        if ChinaTag.is_sz(code):
            return 'sz'
        
        raise Exception("unknown code %s" % code)