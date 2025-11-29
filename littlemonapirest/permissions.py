from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permiso personalizado para permitir solo a los propietarios editar un objeto.
    """
    
    def has_object_permission(self, request, view, obj):
        # Los permisos de lectura se permiten para cualquier request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Los permisos de escritura solo se permiten al propietario
        return obj.name == request.user.get_full_name() or obj.name == request.user.username


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permiso personalizado para permitir solo a los administradores crear/editar/eliminar.
    Los usuarios normales solo pueden leer.
    """
    
    def has_permission(self, request, view):
        # Los permisos de lectura se permiten para cualquier request autenticado
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # Los permisos de escritura solo se permiten a los administradores
        return request.user and request.user.is_staff
