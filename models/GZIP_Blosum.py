import gzip
from .LogFit import LogFit

class GZIP_Blosum(LogFit):

    def encoder(self, string):
        codification = [
            [['C'], "0"],
            [['G'], "1"],
            [['H'], "2"],
            [['P'], "3"],
            [['W'], "4"],
            [['I','L','M','V'], "5"],
            [['K','Q','R','D','E'], "6"],
            [['F','Y'], "7"],
            [['N','T','S','A'], "8"]
        ]

        for codex in codification:
            for letters in codex[0]:
                string = string.replace(letters, codex[1])
        return string

    def compressString(self, string):
        return gzip.compress(bytes(string, 'utf-8'))

    def score(self, groups):
        long_string = ''
        for data_row in groups:
            long_string = str(long_string) + str(self.encoder(data_row))

        return len(self.compressString(long_string))/len(long_string)