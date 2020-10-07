def example(context):
    connection = happybase.Connection('localhost',32794)
    families = {
        'creation': dict(),
        'edition': dict(),
        'name': dict()
    }
    context = {
        'table': connection
    }
    table = context['table']
    print(table.tables(), dir(table.tables()))
    tbl = table.table('snakes')
    print(tbl, dir(tbl))
    tbl.put(
        b'anaconda', 
        {b'creation:':b'now', b'edition:': b'now', b'name:regular': b'anaconda', b'name:type': b'culebra'}
        )
