class Dir:
    def __init__(self, name: str):
        self.name = name
        self.subdirs = []

    def add_subdir(self, subdirs):
        node = self
        for curr in subdirs:
            if curr not in [i.name for i in node.subdirs]:
                curr_dir = Dir(curr)
                node.subdirs.append(curr_dir)
            else:
                curr_dir = [i for i in node.subdirs if i.name == curr][0]
            node = curr_dir

    def print_tree(self, depth=0):
        for subdir in sorted(self.subdirs, key=lambda x: x.name):
            print(' ' * depth + subdir.name)
            subdir.print_tree(depth + 1)
    
    
if __name__ == '__main__':
    n = int(input())
    root = Dir('')
    for _ in range(n):
        path = input().split('\\')
        root.add_subdir(path)
    root.print_tree()