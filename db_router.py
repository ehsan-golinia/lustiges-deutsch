class DatabaseRouter:
    def db_for_read(self, model, **hints):
        """Point database operations for specific apps to MongoDB."""
        if model._meta.app_label in ['Vokabel', 'Singular_Plural']:
            return 'deutschDB'
        return 'default'

    def db_for_write(self, model, **hints):
        """Point writes for specific apps to MongoDB."""
        if model._meta.app_label in ['Vokabel', 'Singular_Plural']:
            return 'deutschDB'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """Allow relations if models are in the same database."""
        db_set = {'default', 'deutschDB'}
        if obj1._state.db in db_set and obj2._state.db in db_set:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Control migrations for each database."""
        if app_label in ['Vokabel', 'Singular_Plural']:
            return db == 'deutschDB'
        return db == 'default'
