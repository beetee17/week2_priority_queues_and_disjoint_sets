# python3

# There are π tables stored in some database. The tables are numbered from 1 to π. All tables share the same set of columns. Each table contains either several rows with real data or a symbolic link toanother table. Initially, all tables contain data, and π-th table has π(π) rows. You need to perform π of the following operations: 
# 1. Consider table number πππ π‘ππππ‘πππ π. Traverse the path of symbolic links to get to the data. That is,while πππ π‘ππππ‘ππππ contains a symbolic link instead of real data do πππ π‘ππππ‘ππππ β symlink(πππ π‘ππππ‘ππππ) 
# 2. Consider the table number π ππ’ππππ and traverse the path of symbolic links from it in the same manner as for πππ π‘ππππ‘ππππ.
# 3. Now, πππ π‘ππππ‘ππππ and π ππ’ππππ are the numbers of two tables with real data. If πππ π‘ππππ‘ππππΜΈ = π ππ’ππππ, copy all the rows from table π ππ’ππππ to table πππ π‘ππππ‘ππππ, then clear the table π ππ’ππππ and instead of real data put a symbolic link to πππ π‘ππππ‘ππππ into it.
# 4. Print the maximum size among all π tables (recall that size is the number of rows in the table).If the table contains only a symbolic link, its size is considered to be 0. See examples and explanations for further clarifications.

# Input Format
# The first line of the input contains two integers π and π β the number of tables in the database and the number of merge queries to perform, respectively.The second line of the input contains π integers ππβ the number of rows in the π-th table.
# Then follow π lines describing merge queries. Each of them contains two integers πππ π‘ππππ‘ππππ and π ππ’ππππβ the numbers of the tables to merge

# Constraints
# 1 β€ π, π β€ 100 000;
# 0 β€ ππ β€ 10 000;
# 1 β€ πππ π‘ππππ‘ππππ, π ππ’ππππ β€π

# Output Format
# For each query print a line containing a single integer β the maximum of the sizes of all tables (in terms of the number of rows) after the corresponding operation.

class Database:
    def __init__(self, row_counts):
        self.row_counts = row_counts
        self.max_row_count = max(row_counts)
        n_tables = len(row_counts)
        self.ranks = [1] * n_tables
        self.parents = list(range(n_tables))

    def merge(self, src, dst):
        src_parent = self.get_parent(src)
        dst_parent = self.get_parent(dst)

        if src_parent == dst_parent:
            return False

        # merge two components
        # use union by rank heuristic
        # update max_row_count with the new maximum table size
        src_rank = self.get_rank(src_parent) 
        dst_rank = self.get_rank(dst_parent)

        if src_rank < dst_rank:
            # hang source sub-tree under destination
            self.set_parent(src_parent, dst_parent)

        elif dst_rank < src_rank:
            # do the opposite as above
            self.set_parent(dst_parent, src_parent)

        else:
            # ranks are equal
            # also hang src sub tree under dst, but update rank by 1
            self.set_parent(src_parent, dst_parent)
            self.set_rank(dst, dst_rank+1)

        return True

    def get_rank(self, table):
        return self.ranks[table]

    def set_rank(self, table, rank):
        self.ranks[table] = rank
        
    def get_parent(self, table):
        # find parent and compress path
        if table != self.parents[table]:
            self.parents[table] = self.get_parent(self.parents[table])
        return self.parents[table]

    def set_parent(self, table, parent):
        self.parents[table] = parent
        self.row_counts[parent] += self.row_counts[table]
        self.row_counts[table] = 0

        if self.row_counts[parent] > self.max_row_count:
            self.set_max(self.row_counts[parent])

    def set_max(self, m):
        self.max_row_count = m


def main():
    n_tables, n_queries = map(int, input().split())
    counts = list(map(int, input().split()))
    assert len(counts) == n_tables
    db = Database(counts)
    for i in range(n_queries):
        dst, src = map(int, input().split())
        db.merge(dst - 1, src - 1)
        print(db.max_row_count)


if __name__ == "__main__":
    main()
