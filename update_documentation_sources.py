#!/usr/bin/env python3
"""
Documentation Source Updater for RAG System
Updates scrapers with current documentation URLs and versions
"""

import os
import json
from pathlib import Path
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentationUpdater:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.updated_sources = {
            'checkmk': {
                'version': '2.3',
                'base_url': 'https://docs.checkmk.com/2.3/en/',
                'guides': [
                    'introduction_installation.html',
                    'introduction_user.html',
                    'introduction_admin.html',
                    'introduction_dev.html',
                    'monitoring_basics.html',
                    'monitoring_hosts_services.html',
                    'notifications.html',
                    'ec_intro.html',
                    'bi_intro.html',
                    'rest_api.html',
                    'agent_intro.html',
                    'changelog.html'
                ]
            },
            'rhel': {
                'version': '9',
                'base_url': 'https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/9/html-single/',
                'guides': [
                    'system_administrators_guide/index',
                    'configuring_and_managing_networking/index',
                    'managing_storage/index',
                    'securing_rhel/index',
                    'installing_using_anaconda/index',
                    'performing_a_standard_rhel_9_installation/index',
                    'upgrading_from_rhel_8_to_rhel_9/index',
                    'managing_software_with_the_dnf_tool/index',
                    'managing_users_and_groups/index',
                    'managing_services_with_systemd/index'
                ]
            },
            'ansible': {
                'version': 'latest',
                'base_url': 'https://docs.ansible.com/ansible/latest/',
                'guides': [
                    'installation_guide/index.html',
                    'user_guide/index.html',
                    'playbook_guide/index.html',
                    'collections_guide/index.html',
                    'inventory_guide/index.html',
                    'galaxy/user_guide.html'
                ]
            },
            'python': {
                'version': '3.12',
                'base_url': 'https://docs.python.org/3.12/',
                'guides': [
                    'tutorial/index.html',
                    'library/index.html',
                    'reference/index.html',
                    'howto/index.html',
                    'library/functions.html',
                    'library/stdtypes.html',
                    'tutorial/inputoutput.html',
                    'tutorial/errors.html'
                ]
            },
            'bash': {
                'version': 'latest',
                'base_url': 'https://www.gnu.org/software/bash/manual/',
                'guides': [
                    'bash.html',
                    'bashref.html',
                    'index.html'
                ]
            },
            'powershell': {
                'version': '7',
                'base_url': 'https://docs.microsoft.com/en-us/powershell/',
                'guides': [
                    'scripting/overview',
                    'scripting/developer/cmdlet/',
                    'scripting/developer/prog-guide/function-provider',
                    'scripting/developer/module/',
                    'scripting/learn/remoting/'
                ]
            },
            'containers': {
                'version': 'latest',
                'base_url': 'https://docs.docker.com/',
                'guides': [
                    'get-started/overview/',
                    'compose/',
                    'engine/swarm/',
                    'docker-hub/'
                ]
            },
            'cybersecurity': {
                'version': 'latest',
                'base_url': 'https://nmap.org/book/',
                'guides': [
                    'index.html',
                    'man.html',
                    'nmap.html'
                ]
            }
        }
    
    def update_scraper(self, technology: str, scraper_path: Path):
        """Update a specific scraper with new documentation sources"""
        if not scraper_path.exists():
            logger.warning(f"Scraper not found: {scraper_path}")
            return False
        
        try:
            # Read the current scraper
            with open(scraper_path, 'r') as f:
                content = f.read()
            
            # Update the doc_sources section
            if technology in self.updated_sources:
                source_config = self.updated_sources[technology]
                
                # Create the new doc_sources dictionary
                new_sources = f"""        self.doc_sources = {{
            '{technology}_docs': {{
                'base_url': '{source_config['base_url']}',
                'guides': {source_config['guides']}
            }}
        }}"""
                
                # Replace the doc_sources section
                import re
                pattern = r'self\.doc_sources\s*=\s*\{[^}]*\}'
                updated_content = re.sub(pattern, new_sources, content, flags=re.DOTALL)
                
                # Write the updated scraper
                with open(scraper_path, 'w') as f:
                    f.write(updated_content)
                
                logger.info(f"Updated {technology} scraper with version {source_config['version']}")
                return True
            else:
                logger.warning(f"No update configuration for {technology}")
                return False
                
        except Exception as e:
            logger.error(f"Error updating {technology} scraper: {e}")
            return False
    
    def update_all_scrapers(self):
        """Update all technology scrapers"""
        results = {}
        
        for technology in self.updated_sources.keys():
            scraper_path = self.base_dir / technology / 'scraper.py'
            results[technology] = self.update_scraper(technology, scraper_path)
        
        return results
    
    def create_update_report(self, results: dict):
        """Create a report of the update process"""
        report = {
            'update_timestamp': datetime.now().isoformat(),
            'results': results,
            'summary': {
                'total_technologies': len(results),
                'successful_updates': sum(1 for success in results.values() if success),
                'failed_updates': sum(1 for success in results.values() if not success)
            }
        }
        
        report_path = self.base_dir / 'documentation_update_report.json'
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Update report saved to {report_path}")
        return report
    
    def check_documentation_availability(self):
        """Check if documentation sources are accessible"""
        import requests
        
        availability_report = {}
        
        for technology, config in self.updated_sources.items():
            try:
                response = requests.head(config['base_url'], timeout=10)
                availability_report[technology] = {
                    'url': config['base_url'],
                    'status_code': response.status_code,
                    'accessible': response.status_code == 200,
                    'version': config['version']
                }
            except Exception as e:
                availability_report[technology] = {
                    'url': config['base_url'],
                    'error': str(e),
                    'accessible': False,
                    'version': config['version']
                }
        
        return availability_report

def main():
    """Main function to update documentation sources"""
    updater = DocumentationUpdater()
    
    print("🔍 Checking documentation availability...")
    availability = updater.check_documentation_availability()
    
    print("\n📊 Documentation Availability Report:")
    for tech, status in availability.items():
        if status['accessible']:
            print(f"✅ {tech.upper()} ({status['version']}): {status['url']}")
        else:
            print(f"❌ {tech.upper()} ({status['version']}): {status.get('error', 'Not accessible')}")
    
    print("\n🔄 Updating scrapers...")
    results = updater.update_all_scrapers()
    
    print("\n📋 Update Results:")
    for tech, success in results.items():
        if success:
            print(f"✅ {tech.upper()}: Updated successfully")
        else:
            print(f"❌ {tech.upper()}: Update failed")
    
    # Create report
    report = updater.create_update_report(results)
    
    print(f"\n📈 Summary:")
    print(f"Total technologies: {report['summary']['total_technologies']}")
    print(f"Successful updates: {report['summary']['successful_updates']}")
    print(f"Failed updates: {report['summary']['failed_updates']}")
    
    print("\n🎯 Next Steps:")
    print("1. Run scrapers to get updated documentation")
    print("2. Re-index documents in each technology")
    print("3. Test RAG systems with updated content")
    print("4. Set up automated updates via cron")

if __name__ == "__main__":
    main()
