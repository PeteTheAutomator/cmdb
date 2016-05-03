CMDB
====

A super-lightweight Config Management Database


Project Status
--------------

Pre-Alpha - really just tinkering at the moment; please don't actually use this :)


Description
-----------

This project sets-up a datastore for recording the configuration of Amazon Linux EC2 Instances; tracking installed RPM packages and various OS details captured using Facter.  The datastore has a REST API powered by Eve and MongoDB.

Also within this project is a client-side tool for harvesting its configuration details and posting them to the CMDB REST API.  The client can simply be scheduled from cron.


Server Installation
-------------------

The CMDB server can be installed using Ansible onto RedHat, CentOS, or Amazon-Linux.  If you're unfamiliar with Ansible I'd suggest you install it on your destination CMDB host for simplicity (rather than your workstation) using this example...

    sudo yum install -y ansible
    
Then clone this git repository onto your destination CMDB host...

    git clone https://github.com/PeteTheAutomator/cmdb.git
    
...and execute the Ansible playbook, within the **deploy** directory...

    cd cmdb/deploy
    ansible-playbook -i 'localhost,' playbook.yml


Client Installation
-------------------

You can install the client using pip - simply point it at this repository like so...

    pip install git+https://github.com/PeteTheAutomator/cmdb.git
    
This provides both the **audit** and **query** CLI tools; both require simple a simple configuration file to be dropped into **/etc/cmdb/server.conf** which should look like the following example...

    [defaults]
    repo_url = http://cmdb-server/audits


Contact
-------

peter.hehn@yahoo.com