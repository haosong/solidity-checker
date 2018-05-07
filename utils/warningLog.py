class Warning:
    def __init__(self, start, end, name):
        self.start = start
        self.end = end
        self.name = name

    def __repr__(self):
        return '%r %r %r' % (self.start, self.end, self.name)

    def __hash__(self):
        return hash(tuple(self.start)) + hash(tuple(self.end)) + hash(tuple(self.name))

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end and self.name == other.end

class WarningLogger:
    def __init__(self, filename):
        f = open(filename, 'r')
        self.lineRanges = []
        self.lines = f.readlines()
        charIdx = 0
        for lineNum, line in enumerate(self.lines):
            line = line.strip('\r\n') + '\r\n' # resolve windows \r\n
            lineEnd = charIdx + len(line)
            self.lineRanges.append((charIdx, lineEnd))
            charIdx = lineEnd
        # print(self.lineRanges)
    
    def log(self, warning):
        start, end, message = warning.start, warning.end, warning.name
        startLine = endLine = 0
        for lineNum, lineRange in enumerate(self.lineRanges):
            if lineRange[0] <= start and start <= lineRange[1]:
                startLine = lineNum
            if lineRange[0] < end and end <= lineRange[1]:
                endLine = lineNum
        print('================================ warning ================================\n')
        if startLine == endLine:
            offset = start - self.lineRanges[startLine][0]
            print(self.lines[startLine].strip('\r\n').strip('\n'))
            print(' ' * offset + '^--' + ' ' + message + ' ' + '\n')
        else:
            for line in self.lines[startLine:endLine + 1]:
                print(line.strip('\n'))
            print('-->' + ' ' + message + ' ' + '\n')
