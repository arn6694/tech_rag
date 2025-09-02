#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))

from base_scraper import BaseDocScraper

class AnsibleScraper(BaseDocScraper):
    def __init__(self):
        super().__init__(
            output_dir="docs",
            technology_name="ansible"
        )
        
        # Based on actual Ansible documentation structure from https://docs.ansible.com/ansible/latest/
        # This covers all major sections comprehensively with verified URLs
        self.doc_sources = {
            "ansible_official": {
                "base_url": "https://docs.ansible.com/ansible/latest/",
                "guides": [
                    # GETTING STARTED (Essential Foundation)
                    "getting_started/index.html",                      # Getting started with Ansible
                    "getting_started/get_started_ansible.html",        # Installation and first steps
                    "getting_started/get_started_inventory.html",      # Your first inventory
                    "getting_started/get_started_playbook.html",       # Creating a playbook
                    "getting_started_ee/index.html",                   # Execution Environments
                    
                    # INSTALLATION & CONFIGURATION (Critical Setup)
                    "installation_guide/index.html",                   # Installation Guide
                    "installation_guide/intro_installation.html",      # Installing Ansible
                    "installation_guide/intro_configuration.html",     # Configuring Ansible
                    
                    # INVENTORY MANAGEMENT (Host Organization)
                    "inventory_guide/index.html",                      # Building Ansible inventories
                    "inventory_guide/intro_inventory.html",            # How to build your inventory
                    "inventory_guide/intro_dynamic_inventory.html",    # Working with dynamic inventory
                    "inventory_guide/intro_patterns.html",             # Patterns: targeting hosts and groups
                    
                    # COMMAND LINE TOOLS (Essential CLI)
                    "command_guide/index.html",                        # Using Ansible command line tools
                    "command_guide/intro_adhoc.html",                  # Introduction to ad hoc commands
                    "command_guide/command_line_tools.html",           # Working with command line tools
                    
                    # PLAYBOOK GUIDE (Core Functionality)
                    "playbook_guide/index.html",                       # Using Ansible playbooks
                    "playbook_guide/playbooks_intro.html",             # Ansible playbooks
                    "playbook_guide/playbooks_variables.html",         # Using variables
                    "playbook_guide/playbooks_conditionals.html",      # Conditionals
                    "playbook_guide/playbooks_loops.html",             # Loops
                    "playbook_guide/playbooks_handlers.html",          # Handlers: running operations on change
                    "playbook_guide/playbooks_error_handling.html",    # Error handling in playbooks
                    "playbook_guide/playbooks_blocks.html",            # Blocks
                    "playbook_guide/playbooks_strategies.html",        # Controlling playbook execution
                    "playbook_guide/playbooks_delegation.html",        # Delegation, rolling updates, and local actions
                    "playbook_guide/playbooks_advanced_syntax.html",   # Advanced syntax features
                    "playbook_guide/playbooks_templating.html",        # Templating (Jinja2)
                    "playbook_guide/playbooks_filters.html",           # Using filters to manipulate data
                    "playbook_guide/playbooks_tests.html",             # Tests
                    "playbook_guide/playbooks_lookups.html",           # Lookups
                    "playbook_guide/playbooks_python_version.html",    # Python version and templating
                    "playbook_guide/playbooks_module_defaults.html",   # Module defaults
                    "playbook_guide/playbooks_privilege_escalation.html", # Understanding privilege escalation
                    "playbook_guide/playbooks_vault.html",             # Using vault in playbooks
                    "playbook_guide/playbooks_tags.html",              # Tags
                    "playbook_guide/playbooks_imports.html",           # Importing playbooks and tasks
                    "playbook_guide/playbooks_reuse.html",             # Re-using Ansible artifacts
                    "playbook_guide/playbooks_reuse_includes.html",    # Including and importing
                    "playbook_guide/playbooks_reuse_roles.html",       # Roles
                    "playbook_guide/complex_data_manipulation.html",   # Manipulating data
                    
                    # VAULT (Security)
                    "vault_guide/index.html",                          # Protecting sensitive data with Ansible vault
                    "vault_guide/vault.html",                          # Using Ansible Vault
                    "vault_guide/vault_encrypting_content.html",       # Encrypting content with Ansible Vault
                    "vault_guide/vault_using_encrypted_content.html",  # Using encrypted variables and files
                    "vault_guide/vault_managing_passwords.html",       # Managing vault passwords
                    
                    # MODULES AND PLUGINS (Extending Functionality)
                    "module_plugin_guide/index.html",                  # Using Ansible modules and plugins
                    "module_plugin_guide/modules_intro.html",          # Introduction to modules
                    "module_plugin_guide/modules_support.html",        # Module maintenance & support
                    "module_plugin_guide/plugin_filtering_config.html", # Plugin filter configuration
                    
                    # COLLECTIONS (Modern Ansible)
                    "collections_guide/index.html",                    # Using Ansible collections
                    "collections_guide/collections_installing.html",   # Installing collections
                    "collections_guide/collections_using.html",        # Using collections in a playbook
                    "collections_guide/collections_using_playbooks.html", # Using collections in playbooks
                    "collections_guide/collections_downloading.html",  # Downloading collections for offline use
                    "collections_guide/collections_listing.html",      # List installed collections
                    "collections_guide/collections_verifying.html",    # Verifying collections
                    
                    # OS-SPECIFIC GUIDES (Platform Support)
                    "os_guide/index.html",                             # Using Ansible on Windows, BSD, and z/OS UNIX
                    "os_guide/windows.html",                           # Using Ansible to manage Windows systems
                    "os_guide/windows_setup.html",                     # Setting up a Windows host
                    "os_guide/windows_usage.html",                     # Using Ansible with Windows
                    "os_guide/windows_winrm.html",                     # Windows Remote Management
                    "os_guide/windows_dsc.html",                       # Windows PowerShell DSC
                    "os_guide/windows_faq.html",                       # Windows FAQ
                    
                    # TIPS AND TRICKS (Best Practices)
                    "tips_tricks/index.html",                          # Ansible tips and tricks
                    "tips_tricks/ansible_tips_tricks.html",            # General tips
                    "tips_tricks/sample_setup.html",                   # Sample Ansible setup
                    
                    # NETWORK AUTOMATION (Infrastructure)
                    "network/getting_started/index.html",              # Network Getting Started
                    "network/getting_started/first_playbook.html",     # Run Your First Command and Playbook  
                    "network/getting_started/first_inventory.html",    # Build Your Inventory
                    "network/getting_started/network_roles.html",      # Use Ansible network roles
                    "network/getting_started/network_connection_options.html", # Working with network connection options
                    "network/user_guide/index.html",                   # Network Advanced Topics
                    "network/user_guide/network_best_practices_2.5.html", # Network Best Practices for Ansible 2.5
                    "network/user_guide/network_debug_troubleshooting.html", # Network Debug and Troubleshooting Guide
                    "network/user_guide/cli_parsing.html",             # Parsing semi-structured text with Ansible
                    "network/user_guide/validate.html",                # Validate data against set criteria with Ansible
                    "network/user_guide/network_working_with_command_output.html", # Working with command output
                    
                    # DEVELOPER GUIDE (Advanced Topics)
                    "dev_guide/index.html",                            # Developer Guide  
                    "dev_guide/developing_locally.html",               # Adding modules and plugins locally
                    "dev_guide/developing_modules.html",               # Should you develop a module?
                    "dev_guide/developing_modules_general.html",       # Developing modules
                    "dev_guide/developing_modules_checklist.html",     # Contributing your module
                    "dev_guide/developing_modules_best_practices.html", # Conventions, tips, and pitfalls
                    "dev_guide/developing_python_3.html",              # Ansible and Python 3
                    "dev_guide/debugging.html",                        # Debugging modules
                    "dev_guide/developing_modules_documenting.html",   # Module format and documentation
                    "dev_guide/developing_plugins.html",               # Developing plugins
                    "dev_guide/developing_inventory.html",             # Developing dynamic inventory
                    "dev_guide/developing_api.html",                   # Python API
                    "dev_guide/developing_module_utilities.html",      # Using and developing module utilities
                    "dev_guide/developing_collections.html",           # Developing collections
                    "dev_guide/testing.html",                          # Testing Ansible
                    "dev_guide/overview_architecture.html",            # Ansible architecture
                    
                    # REFERENCE AND CONFIGURATION (Technical Details)
                    "reference_appendices/config.html",                # Ansible Configuration Settings
                    "reference_appendices/general_precedence.html",    # Controlling how Ansible behaves
                    "reference_appendices/playbooks_keywords.html",    # Playbook Keywords
                    "reference_appendices/common_return_values.html",  # Return Values
                    "reference_appendices/YAMLSyntax.html",            # YAML Syntax
                    "reference_appendices/python_3_support.html",      # Python 3 Support
                    "reference_appendices/interpreter_discovery.html", # Interpreter Discovery
                    "reference_appendices/special_variables.html",     # Special Variables
                    "reference_appendices/faq.html",                   # Frequently Asked Questions
                    "reference_appendices/glossary.html",              # Glossary
                    "reference_appendices/test_strategies.html",       # Testing Strategies
                    "reference_appendices/logging.html",               # Logging Ansible output
                    
                    # COMMUNITY AND CONTRIBUTION (Collaboration)
                    "community/index.html",                            # Ansible Community Guide
                    "community/contributions.html",                    # ansible-core Contributors Guide
                    "community/contributions_collections.html",        # Ansible Collections Contributor Guide
                    "community/reporting_collections.html",            # Requesting changes to a collection
                    "community/create_pr_quick_start.html",            # Creating your first collection pull request
                    "community/documentation_contributions.html",      # Contributing to the Ansible Documentation
                    
                    # PORTING GUIDES (Version Migration)
                    "porting_guides/porting_guides.html",              # Ansible Porting Guides
                    "porting_guides/porting_guide_11.html",            # Ansible 11 Porting Guide
                    "porting_guides/porting_guide_10.html",            # Ansible 10 Porting Guide
                    "porting_guides/porting_guide_9.html",             # Ansible 9 Porting Guide
                    "porting_guides/porting_guide_8.html",             # Ansible 8 Porting Guide
                ]
            }
        }
        
        # Configuration for intelligent link discovery
        self.scraping_config = {
            'follow_internal_links': True,
            'max_depth': 2,
            'delay_between_requests': 1.0,
            'include_patterns': [
                '/ansible/latest/',
                'playbook_guide/',
                'user_guide/',
                'inventory_guide/',
                'getting_started/',
                'installation_guide/',
                'vault_guide/',
                'collections_guide/',
                'module_plugin_guide/',
                'dev_guide/',
                'network/',
                'reference_appendices/',
                'community/'
            ],
            'exclude_patterns': [
                '/devel/',           # Development versions
                '/2.9/',            # Old versions  
                '/2.8/',            # Old versions
                '/2.7/',            # Old versions
                'roadmap/',         # Roadmap content
                'galaxy/',          # Galaxy-specific
                'tower.html',       # Tower/AAP specific
                'automationhub.html' # Automation Hub specific
            ]
        }

    def should_skip_url(self, url):
        """Check if URL should be skipped based on exclusion patterns"""
        for pattern in self.scraping_config['exclude_patterns']:
            if pattern in url:
                return True
        return False

    def extract_additional_links(self, soup, base_url):
        """Extract additional relevant Ansible documentation links"""
        additional_links = []
        
        # Look for links in main content areas
        content_areas = soup.find_all(['main', 'div'], class_=['main', 'content', 'document', 'body'])
        if not content_areas:
            content_areas = [soup.find('body')] if soup.find('body') else [soup]
        
        for content_area in content_areas:
            if content_area:
                for link in content_area.find_all('a', href=True):
                    href = link.get('href')
                    
                    # Convert relative URLs to absolute
                    if href.startswith('/'):
                        full_url = f"https://docs.ansible.com{href}"
                    elif href.startswith('http'):
                        full_url = href
                    elif href.endswith('.html'):
                        full_url = base_url.rsplit('/', 1)[0] + '/' + href
                    else:
                        continue
                    
                    # Check if this link should be included
                    if (not self.should_skip_url(full_url) and 
                        full_url not in self.scraped_urls and
                        any(pattern in full_url for pattern in self.scraping_config['include_patterns'])):
                        additional_links.append(full_url)
        
        # Limit additional links to prevent overwhelming
        return additional_links[:15]

    def get_page_priority(self, url):
        """Determine scraping priority based on URL content"""
        priority_keywords = {
            'getting_started': 10,
            'playbook_guide': 10,
            'installation_guide': 9,
            'inventory_guide': 9,
            'playbooks_intro': 9,
            'playbooks_variables': 8,
            'playbooks_conditionals': 8,
            'playbooks_loops': 8,
            'vault': 7,
            'collections': 7,
            'modules': 6,
            'network': 6,
            'dev_guide': 5,
        }
        
        for keyword, priority in priority_keywords.items():
            if keyword in url:
                return priority
        
        return 4  # Default priority

    def extract_content(self, soup, url):
        """Enhanced content extraction for Ansible documentation"""
        # Call parent method first
        content = super().extract_content(soup, url)
        
        if content:
            # Extract Ansible-specific elements
            
            # Extract code blocks and examples (very important for Ansible)
            code_examples = []
            for code_block in soup.find_all(['pre', 'code']):
                code_text = code_block.get_text().strip()
                if len(code_text) > 20:  # Meaningful code blocks
                    code_examples.append(code_text)
            
            # Extract YAML examples (critical for Ansible)
            yaml_examples = []
            for code_block in soup.find_all('pre'):
                code_text = code_block.get_text().strip()
                if ('---' in code_text or 'name:' in code_text or 
                    'hosts:' in code_text or 'tasks:' in code_text):
                    yaml_examples.append(code_text)
            
            # Extract command examples
            command_examples = []
            for code_block in soup.find_all(['pre', 'code']):
                code_text = code_block.get_text().strip()
                if any(cmd in code_text for cmd in ['ansible ', 'ansible-playbook ', 'ansible-vault ', 'ansible-doc ']):
                    command_examples.append(code_text)
            
            # Extract section headers for better organization
            sections = []
            for header in soup.find_all(['h1', 'h2', 'h3', 'h4']):
                header_text = header.get_text().strip()
                if header_text and len(header_text) < 200:
                    sections.append(header_text)
            
            # Add Ansible-specific metadata
            content.update({
                'code_examples': code_examples,
                'yaml_examples': yaml_examples, 
                'command_examples': command_examples,
                'sections': sections,
                'ansible_keywords': self.extract_ansible_keywords(content['content'])
            })
        
        return content

    def extract_ansible_keywords(self, text):
        """Extract Ansible-specific keywords for better categorization"""
        ansible_keywords = [
            'playbook', 'inventory', 'tasks', 'handlers', 'roles', 'vars', 'templates',
            'modules', 'plugins', 'collections', 'vault', 'galaxy', 'facts',
            'conditionals', 'loops', 'blocks', 'tags', 'includes', 'imports'
        ]
        
        found_keywords = []
        text_lower = text.lower()
        for keyword in ansible_keywords:
            if keyword in text_lower:
                found_keywords.append(keyword)
        
        return found_keywords

if __name__ == "__main__":
    print("Starting Comprehensive Ansible Documentation Scraper")
    print("="*60)
    print("This scraper will collect extensive Ansible documentation including:")
    print("- Getting Started guides")
    print("- Installation and Configuration")  
    print("- Playbook development")
    print("- Inventory management")
    print("- Vault security")
    print("- Collections and modules")
    print("- Network automation")
    print("- Developer guides")
    print("- Best practices and tips")
    print("- Reference materials")
    print("="*60)
    
    scraper = AnsibleScraper()
    scraper.scrape_documentation()
    
    print("\n" + "="*60)
    print("Ansible documentation scraping completed!")
    print("Expected result: 100+ comprehensive documentation pages")
    print("Next steps:")
    print("1. Run: python3 rag_system.py --index")
    print("2. Start API: python3 api_server.py") 
    print("3. Add http://localhost:8001 to Open WebUI")
    print("="*60)
