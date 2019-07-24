class MultigtfsRouter:
    """
    A router to control all database operations on models in the
    gtfs application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read gtfs models go to spatialdb.
        """
        if model._meta.app_label == 'multigtfs':
            return 'spatialdb'
        return 'default'

    def db_for_write(self, model, **hints):
        """
        Attempts to write gtfs models go to spatialdb.
        """
        if model._meta.app_label == 'multigtfs':
            return 'spatialdb'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the gtfs app is involved.
        """
        if obj1._meta.app_label == 'multigtfs' or \
           obj2._meta.app_label == 'multigtfs':
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the gtfs app only appears in the 'spatialdb'
        database.
        """
        if app_label == 'multigtfs':
            return db == 'spatialdb'
        return 'default'

class DefaultRouter:
    def db_for_read(self, model, **hints):
        """
        Reads go to default.
        """
        return 'spatialdb'

    def db_for_write(self, model, **hints):
        """
        Writes always go to default.
        """
        return 'spatialdb'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Relations between objects are allowed.
        """
        db_list = ('default', 'spatialdb')
        if obj1._state.db in db_list and obj2._state.db in db_list:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        All non-spatial models end up in this pool.
        """
        return True