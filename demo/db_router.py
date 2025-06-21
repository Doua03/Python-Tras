class ActorDatabaseRouter:
    def db_for_read(self, model, **hints):
        """
        Direct read operations to the appropriate database based on the model's actor type.
        """
        if model._meta.app_label == 'admin':
            return 'admin_db'
        elif model._meta.app_label == 'user':
            return 'user_db'
        elif model._meta.app_label == 'doctor':
            return 'doctor_db'
        return 'default'  # Default database for common models

    def db_for_write(self, model, **hints):
        """
        Direct write operations to the appropriate database based on the model's actor type.
        """
        if model._meta.app_label == 'admin':
            return 'admin_db'
        elif model._meta.app_label == 'user':
            return 'user_db'
        elif model._meta.app_label == 'doctor':
            return 'doctor_db'
        return 'default'

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Allow migrations only to the relevant database.
        """
        if db == 'default':
            return True  # Migrations for shared models go to default database
        if app_label == 'admin' and db == 'admin_db':
            return True
        if app_label == 'user' and db == 'user_db':
            return True
        if app_label == 'doctor' and db == 'doctor_db':
            return True
        return False
