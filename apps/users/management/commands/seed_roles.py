from django.core.management.base import BaseCommand
from apps.users.models import Role


class Command(BaseCommand):
    
    def handle(self, *args, **kwargs):
        
        roles = [
            {
                'name': 'admin',
                'description': 'System administrator'
            },
            {
                'name': 'teamlead',
                'description': 'Team Lead'
            },
            {
                'name': 'user',
                'description': 'Normal User'
            }
        ]
        
        for role_data in roles:
            Role.objects.get_or_create(
                name=role_data['name'],
                defaults={
                    'description': role_data['description']
                }
            )
            
            
        self.stdout.write(
            self.style.SUCCESS("Roles Seeded Successfully")
        )