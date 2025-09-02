#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))

from base_scraper import BaseDocScraper

class CheckmkScraper(BaseDocScraper):
    def __init__(self):
        super().__init__(
            output_dir="docs",
            technology_name="checkmk"
        )
        
        # Based on actual CheckMK documentation structure - verified URLs only
        # Focusing on: deployment, installation, upgrading, troubleshooting, automation, API/REST API usage, advanced subjects
        # Excluding: cloud deployment, versions older than 2.3
        self.doc_sources = {
            "checkmk_latest": {
                "base_url": "https://docs.checkmk.com/latest/en/",
                "guides": [
                    # INSTALLATION & DEPLOYMENT (Priority 1)
                    "intro_setup.html",                    # CheckMK setup and first installation
                    "install_packages_debian.html",        # Debian/Ubuntu installation  
                    "install_packages_redhat.html",        # RHEL/CentOS installation
                    "install_packages_sles.html",          # SUSE installation
                    "introduction_docker.html",            # Docker installation
                    "appliance_install_virt1.html",        # Virtual appliance installation
                    "intro_setup_monitor.html",            # Setting up monitoring
                    
                    # UPGRADING & UPDATES (Priority 1)
                    "update.html",                          # Updates and upgrades main guide
                    "update_major.html",                    # Major version updates
                    "update_matrix.html",                   # Version compatibility matrix
                    "release_upgrade.html",                # Linux distribution upgrades
                    
                    # API & REST API USAGE (Priority 1) 
                    "rest_api.html",                        # Complete REST API documentation
                    "apis_intro.html",                      # Overview of all APIs
                    "livestatus.html",                      # Livestatus API
                    "livestatus_references.html",          # Livestatus command reference
                    
                    # AGENT MANAGEMENT (Priority 1)
                    "agent_linux.html",                    # Linux agent installation and management
                    "agent_windows.html",                  # Windows agent installation and management
                    "agent_deployment.html",               # Automatic agent updates and deployment
                    "wato_monitoringagents.html",          # Agent configuration through WATO
                    
                    # TROUBLESHOOTING (Priority 2)
                    "analyze_configuration.html",          # Configuration analysis tools
                    "support_diagnostics.html",            # Support diagnostics
                    "omd_basics.html",                     # Site administration with omd
                    "commands.html",                        # Command line tools
                    
                    # ADVANCED TOPICS (Priority 2)
                    "distributed_monitoring.html",         # Distributed monitoring setup
                    "dcd.html",                            # Dynamic host management
                    "ec.html",                             # Event Console
                    "appliance_usage.html",                # Appliance configuration and usage
                    "managed.html",                        # CheckMK Managed Services (MSP)
                    "wato_user.html",                      # User management and permissions
                    "snmp.html",                           # SNMP monitoring
                    
                    # MONITORING SETUP & CONFIGURATION (Priority 2)
                    "hosts_setup.html",                    # Host administration
                    "labels.html",                         # Labels for organization
                    "rules.html",                          # Rules configuration
                    "services.html",                       # Service configuration
                    "monitoring_basics.html",              # Basic monitoring concepts
                    "wato_hosts.html",                     # Host configuration
                    "wato_services.html",                  # Service configuration
                    "discovery.html",                      # Service discovery
                    
                    # SYSTEM ADMINISTRATION (Priority 3)
                    "backup.html",                         # Backup procedures
                    "security.html",                       # Security configuration
                    "ports.html",                          # Port configuration
                    "timeperiods.html",                    # Time periods configuration
                    "ldap.html",                           # LDAP integration
                    "kerberos.html",                       # Kerberos authentication
                    "saml.html",                           # SAML authentication
                    
                    # MONITORING TECHNOLOGIES (Priority 3)
                    "monitoring_docker.html",              # Docker monitoring
                    "monitoring_kubernetes.html",          # Kubernetes monitoring  
                    "monitoring_vmware.html",              # VMware monitoring
                    "monitoring_windows.html",             # Windows monitoring specifics
                    "monitoring_network.html",             # Network monitoring
                    "monitoring_via_ssh.html",             # SSH-based monitoring
                    
                    # AUTOMATION & INTEGRATION (Priority 3)
                    "automation.html",                     # Automation capabilities
                    "web_api.html",                        # Web API usage
                    "mkps.html",                           # Extension packages
                    "check_plugins.html",                  # Check plugin development
                    "special_agents.html",                 # Special agents
                    "datasource_programs.html",            # Data source programs
                    "piggyback.html",                      # Piggyback mechanism
                    "active_checks.html",                  # Active checks
                    "localchecks.html",                    # Local checks
                    "mrpe.html",                           # MK's Remote Plugin Executor
                    
                    # PERFORMANCE & MONITORING (Priority 3)
                    "graphing.html",                       # Performance graphing
                    "metrics.html",                        # Metrics collection
                    "reporting.html",                      # Reporting features
                    "influxdb.html",                       # InfluxDB integration
                    "prometheus.html",                     # Prometheus integration
                    "ntopng_integration.html",             # ntopng integration
                    
                    # NOTIFICATIONS & ALERTING (Priority 3)
                    "notifications.html",                  # Notification configuration
                    "alert_handlers.html",                 # Alert handling
                    "escalations.html",                    # Escalation procedures
                    
                    # USER INTERFACE (Priority 3)
                    "views.html",                          # Custom views
                    "dashboards.html",                     # Dashboard creation
                    "bi.html",                            # Business Intelligence
                    "user_interface.html",                # User interface guide
                    "sidebar.html",                        # Sidebar configuration
                    
                    # ADDITIONAL FEATURES (Priority 3)
                    "inventory.html",                      # Hardware/Software inventory
                    "two_factor_authentication.html",      # 2FA setup
                    "sound.html",                          # Sound notifications
                ]
            },
            
            # CheckMK 2.3.0 specific documentation 
            "checkmk_2_3_0": {
                "base_url": "https://docs.checkmk.com/2.3.0/en/",
                "guides": [
                    # Focus on the most important 2.3.0-specific content
                    # INSTALLATION & DEPLOYMENT
                    "intro_setup.html",
                    "install_packages_debian.html",
                    "install_packages_redhat.html", 
                    "install_packages_sles.html",
                    "introduction_docker.html",
                    "appliance_install_virt1.html",
                    "intro_setup_monitor.html",
                    
                    # UPGRADING & UPDATES
                    "update.html",
                    "update_major.html", 
                    "update_matrix.html",
                    "release_upgrade.html",
                    
                    # API & REST API USAGE
                    "rest_api.html",
                    "apis_intro.html",
                    "livestatus.html",
                    "livestatus_references.html",
                    
                    # AGENT MANAGEMENT
                    "agent_linux.html",
                    "agent_windows.html",
                    "agent_deployment.html",
                    
                    # TROUBLESHOOTING
                    "analyze_configuration.html",
                    "support_diagnostics.html",
                    "omd_basics.html",
                    "commands.html",
                    
                    # ADVANCED TOPICS
                    "distributed_monitoring.html",
                    "dcd.html",
                    "ec.html",
                    "appliance_usage.html",
                    "wato_user.html",
                    "snmp.html",
                    
                    # CORE MONITORING SETUP
                    "hosts_setup.html",
                    "labels.html",
                    "rules.html",
                    "services.html",
                    "monitoring_basics.html",
                ]
            }
        }
        
        # Additional scraping configuration
        self.scraping_config = {
            'follow_internal_links': True,          # Follow links within CheckMK docs
            'max_depth': 2,                         # Maximum link following depth
            'delay_between_requests': 1.0,          # Rate limiting
            'exclude_patterns': [
                '/de/',                             # German content
                '/fr/',                             # French content
                '/es/',                             # Spanish content  
                '/2.0.',                            # Version 2.0.x
                '/2.1.',                            # Version 2.1.x
                '/2.2.',                            # Version 2.2.x
                'cloud_',                           # Cloud-specific content
                'aws_',                             # AWS-specific content
                'azure_',                           # Azure-specific content
                'gcp_',                             # GCP-specific content
            ],
            'include_patterns': [
                '/en/intro_',                       # Introduction guides
                '/en/install_',                     # Installation guides
                '/en/agent_',                       # Agent documentation
                '/en/rest_api',                     # REST API docs
                '/en/update',                       # Update procedures
                '/en/upgrade',                      # Upgrade procedures
                '/en/troubleshoot',                 # Troubleshooting
                '/en/distributed_',                 # Distributed monitoring
                '/en/automation',                   # Automation
                '/en/api',                          # API documentation
                '/en/omd_',                         # OMD administration
                '/en/appliance_',                   # Appliance management
                '/en/dcd',                          # Dynamic configuration
                '/en/ec',                           # Event console
                '/en/snmp',                         # SNMP monitoring
                '/en/hosts_',                       # Host management
                '/en/services',                     # Service configuration
                '/en/rules',                        # Rules configuration
                '/en/labels',                       # Labels
                '/en/wato_',                        # WATO configuration
                '/en/commands',                     # Command line tools
            ]
        }

    def should_skip_url(self, url):
        """
        Check if URL should be skipped based on exclusion patterns
        """
        # Skip URLs with exclusion patterns
        for pattern in self.scraping_config['exclude_patterns']:
            if pattern in url:
                return True
        
        # Only include URLs with inclusion patterns (if any match)
        if self.scraping_config['include_patterns']:
            for pattern in self.scraping_config['include_patterns']:
                if pattern in url:
                    return False
            # If no inclusion patterns match, skip the URL
            return True
        
        return False

    def extract_additional_links(self, soup, base_url):
        """
        Extract additional relevant links from scraped pages
        Override base method to add CheckMK-specific link extraction
        """
        additional_links = []
        
        # Look for links in content area that match our focus areas
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            
            # Convert relative URLs to absolute
            if href.startswith('/'):
                full_url = f"https://docs.checkmk.com{href}"
            elif href.startswith('http'):
                full_url = href
            else:
                full_url = base_url.rsplit('/', 1)[0] + '/' + href
            
            # Check if this link should be included
            if not self.should_skip_url(full_url) and full_url not in self.scraped_urls:
                additional_links.append(full_url)
        
        return additional_links[:10]  # Limit to 10 additional links per page

    def get_page_priority(self, url):
        """
        Determine page priority based on URL content
        Higher priority pages are scraped first
        """
        priority_keywords = {
            'intro_setup': 10,
            'install_': 10,
            'rest_api': 10,
            'agent_': 9,
            'update': 9,
            'upgrade': 9,
            'troubleshoot': 8,
            'distributed_': 7,
            'automation': 7,
            'api': 7,
        }
        
        for keyword, priority in priority_keywords.items():
            if keyword in url:
                return priority
        
        return 5  # Default priority

if __name__ == "__main__":
    print("Starting CheckMK Documentation Scraper")
    print("Focus areas: deployment, installation, upgrading, troubleshooting, automation, API/REST API usage, advanced subjects")
    print("Excluding: cloud deployment, versions older than 2.3")
    print("Scraping from latest and 2.3.0 documentation...")
    
    scraper = CheckmkScraper()
    scraper.scrape_documentation()
    
    print("CheckMK documentation scraping completed!")
    print("Next steps:")
    print("1. Run: python3 rag_system.py --index")
    print("2. Start API: python3 api_server.py")
    print("3. Add http://localhost:8002 to Open WebUI")
