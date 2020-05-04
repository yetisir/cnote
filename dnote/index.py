from whoosh import index, writing, reading, matching


class DynamoDBIndex(index.Index):
    def __init__(self, schema, table_name, **kwargs):
        super().__init__(**kwargs)

        self.schema = schema
        self.table_name = table_name
        self.table = None  # ********8

    def is_empty(self):
        return self.table.item_count() == 0

    def reader(self, **kwargs):
        return DynamoDBReader(self.schema)

    def writer(self, **kwargs):
        return DynamoDBWriter(self.schema)


class DynamoDBWriter(writing.IndexWriter):
    def __init__(self, schema, **kwargs):
        super().__init__(**kwargs)
        self.schema = schema

    def add_document(self, **fields):
        pass

    def add_reader(self):
        pass


class DynamoDBReader(reading.IndexReader):
    def __contains__(self):
        pass

    def __iter__(self):
        pass

    def stored_fields(self):
        pass

    def doc_count_all(self):
        pass

    def doc_count(self):
        pass

    def doc_field_length(self):
        pass

    def field_length(self):
        pass

    def max_field_length(self):
        pass

    def postings(self):
        pass

    def has_vector(self):
        pass

    def vector(self):
        pass

    def doc_frequency(self):
        pass

    def frequency(self):
        pass


class DynamoDBMatcher(matching.Matcher):
    def is_active():
        pass

    def copy(self):
        pass

    def id(self):
        pass

    def next(self):
        pass

    def value(self):
        pass

    def value_as(self):
        pass

    def score(self):
        pass


class DynamoDBStorage(Storage):
    """Storage object that keeps the index in memory.
    """

    supports_mmap = False

    def __init__(self):
        self.files = {}
        self.locks = {}
        self.folder = ''

    def destroy(self):
        del self.files
        del self.locks

    def list(self):
        return list(self.files.keys())

    def clean(self):
        self.files = {}

    def total_size(self):
        return sum(self.file_length(f) for f in self.list())

    def file_exists(self, name):
        return name in self.files

    def file_length(self, name):
        if name not in self.files:
            raise NameError(name)
        return len(self.files[name])

    def file_modified(self, name):
        return -1

    def delete_file(self, name):
        if name not in self.files:
            raise NameError(name)
        del self.files[name]

    def rename_file(self, name, newname, safe=False):
        if name not in self.files:
            raise NameError(name)
        if safe and newname in self.files:
            raise NameError("File %r exists" % newname)

        content = self.files[name]
        del self.files[name]
        self.files[newname] = content

    def create_file(self, name, **kwargs):
        def onclose_fn(sfile):
            self.files[name] = sfile.file.getvalue()
        f = StructFile(BytesIO(), name=name, onclose=onclose_fn)
        return f

    def open_file(self, name, **kwargs):
        if name not in self.files:
            raise NameError(name)
        buf = memoryview_(self.files[name])
        return BufferFile(buf, name=name, **kwargs)

    def lock(self, name):
        if name not in self.locks:
            self.locks[name] = Lock()
        return self.locks[name]

    def temp_storage(self, name=None):
        tdir = tempfile.gettempdir()
        name = name or "%s.tmp" % random_name()
        path = os.path.join(tdir, name)
        tempstore = FileStorage(path)
        return tempstore.create()

