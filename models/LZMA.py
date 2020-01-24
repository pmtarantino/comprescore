import lzma
from .LogFit import LogFit

class LZMA(LogFit):

    def encoder(self, string):
        return string

    def compressString(self, string):
        return lzma.compress(bytes(string, 'utf-8'))

    def score(self, groups):
        long_string = ''
        for data_row in groups:
            long_string = str(long_string) + str(self.encoder(data_row))
        return len(self.compressString(long_string))/len(long_string)