# from datetime import datetime
import uuid
import shutil
import os
import json
import subprocess
import sys
# from subprocess import check_output

class AKSTerraform():
    def __init__(self, source_manifest_path, storage_account, storage_container, variables=None):
        self.name = os.path.basename(source_manifest_path).split(".")[0]
        # print("Manifest name:" + self.name)
        self.object_id = str(uuid.uuid4())
        self.source_manifest_path = source_manifest_path
        print(self.source_manifest_path)
        self.tmpdir = os.path.join(".", "." + self.object_id)
        print(self.tmpdir)
        self.manifestdir = os.path.join(self.tmpdir, self.name)
        print(self.manifestdir)
        self.state_path = os.path.join(self.manifestdir, "terraform.tfstate")
        print(self.state_path)
        self.AKS_State_str = self.set_AKS_State(storage_account, storage_container)
        self.AKS_Plan_str = self.set_AKS_Plan("/out.plan")
        self.AKS_Apply_str = self.set_AKS_Apply("/out.plan")
        self.variables = ""
        self.copy_tmp_manifest()
        self.variables = self.parse_variables(variables)
        print("Variables: ",variables)
        self.generate_vars_file()
        init(self)
        plan(self)
        apply(self)
        self.remove_tmp_manifest()

    def cleanup(self):
        self.remove_tmp_manifest()

    def is_a_terraform_file(self, f):
        return (os.path.isfile(f) and (f.lower().endswith(".tf") or f.lower().endswith(".tf.json")))

    def copy_tmp_manifest(self):
        if os.path.isdir(self.source_manifest_path):
            files = [f for f in os.listdir(self.source_manifest_path) if self.is_a_terraform_file(os.path.join(self.source_manifest_path, f))]
            if len(files) > 0:
                if not os.path.isdir(self.tmpdir):
                    os.mkdir(self.tmpdir)
                shutil.copytree(self.source_manifest_path, os.path.join(self.tmpdir, self.name))
            else:
                raise(Exception("Terraform files not found.  Must have at least one *.tf or *.tf.json file to feed to Terraform."))
        elif self.is_a_terraform_file(self.source_manifest_path):
            if not os.path.isdir(self.tmpdir):
                os.mkdir(self.tmpdir)
            if not os.path.isdir(self.manifestdir):
                os.mkdir(self.manifestdir)
            shutil.copy(self.source_manifest_path, self.manifestdir)
        else:
            raise(Exception("Manifest file not found.  Must have a *.tf or *.tf.json file to feed to Terraform."))

    def generate_vars_file(self):
        with open(os.path.join(self.manifestdir, 'variables.tf'), 'w') as vars_file:
            vars_file.write(self.variables)
        vars_file.close()

    def remove_tmp_manifest(self):
        if os.path.isdir(self.tmpdir):
            shutil.rmtree(self.tmpdir)

    def set_AKS_State(self, StorageAccount, StorageContainer):
        account_Str = "-backend-config="  + "'" +  "storage_account_name=" + StorageAccount + "'"
        container_Str = "-backend-config="  + "'" +  "container_name=" + StorageContainer + "'"
        return account_Str + " " + container_Str

    def set_AKS_Plan(self, PlanStr):
        AKS_plan_str = "-out " + self.manifestdir + PlanStr
        return AKS_plan_str

    def set_AKS_Apply(self, ApplyStr):
        AKS_apply_str = self.manifestdir + ApplyStr
        return AKS_apply_str

    def state(self):
        retval = {}
        if os.path.isfile(self.state_path):
            with open(self.state_path, 'r') as state_file:
                retval = json.load(state_file)
            state_file.close()
        return retval

    def old_apply(self):
        self.current_stats = {}
        cmd = "terraform apply -input=false -state=" + self.state_path  + " " + self.manifestdir
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=1, shell=True)
        output = self.parse_output(p)
        p.stdout.close()
        return output

    def destroy(self):
        self.current_stats = {}
        cmd = "terraform destroy -input=false -force -state=" + self.state_path  + " " + self.manifestdir
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=1, shell=True)
        output = self.parse_output(p)
        p.stdout.close()
        return output

    def parse_output(self, process):
        retval = {
            "start_times": {},
            "durations": {}
        }
        #for line in iter(process.stdout.readline, b''):
            #if "Creating..." in line or "Destroying..." in line:
                # object_name = line.split(": ")[0].replace('\x1b[0m\x1b[1m','')
                #retval['start_times'][object_name] = datetime.utcnow()
                # print line.strip() + ", starting at " + str(retval['start_times'][object_name]) + "\n"
            #elif "Creation complete" in line or "Destruction complete" in line:
                # object_name = line.split(": ")[0].replace('\x1b[0m\x1b[1m','')
                #retval['durations'][object_name] = datetime.utcnow() - retval['start_times'][object_name]
                # print line.strip() + ", with duration " + str(retval['durations'][object_name]) + "\n"
            #else:
                # print line
        return retval

    def parse_variables(self, variables):
        if variables is not None:
            tf_vars = ""
            for variable in variables:
                innerV = variables[variable]
                print(variable, innerV)
                if isinstance(innerV, int):
                    tf_vars = tf_vars + "variable \"" + variable + "\" " + "{" + "\n" + "  default = " \
                              + str(innerV) + "\n" + "}" + "\n" + "\n"
                else:
                    tf_vars = tf_vars + "variable \"" + variable + "\" " + "{" + "\n" + "  default = " \
                              + "\"" + innerV + "\"" + "\n" + "}" + "\n" + "\n"
            return tf_vars
        else:
            return None

def init(self):
    tf_cmd = "Terraform init" + " " + self.AKS_State_str + " " + self.manifestdir
    print(tf_cmd)
    tf_command_helper(tf_cmd)

def plan(self):
    tf_cmd = "Terraform plan" + " " + self.AKS_Plan_str + " " + self.manifestdir
    print(tf_cmd)
    tf_command_helper(tf_cmd)

def apply(self):
    tf_cmd = "Terraform apply" + " " + self.AKS_Apply_str
    print(tf_cmd)
    tf_command_helper(tf_cmd)

###########################################################################################################
# K8S Command helpers and builders provide an ability to wrap Command line and API calls for K8S
# will create helper class
###########################################################################################################
def tf_command_builder(self, command):
    """
    Kubernetes Command Builder mpw v0.7
    accepts kubernetes cluster command
    returns custom command based on JSON values
    :param self, command:
    :return:
    """
    # create sub-command strings
    # return fully qualified kubernetes shell commands
    return {
            'create': 'kops create cluster' + ' ' + self.SubDomain + ' ' + self.CloudType + ' ' + self.State + ' '
                      + self.Zones + ' ' + self.NodeCount + ' ' + self.MasterSize + ' ' + self.NodeSize + ' '
                      + self.DNSZones,
            'delete': 'kops delete cluster' + ' ' + self.SubDomain + ' ' + self.State + ' ' + self.Yes,
            'update': 'kops update cluster' + ' ' + self.SubDomain + ' ' + self.State + ' ' + self.Yes,
            'validate': 'kops validate cluster' + ' ' + self.SubDomain + ' ' + self.State,
            'rolling-update': 'kops rolling-update cluster' + ' ' + self.SubDomain + ' ' + self.State + ' '
                              + self.Yes,
            'get deployments': 'kubectl' + ' ' + command,
            'get pods': 'kubectl' + ' ' + command,
            'get nodes': 'kubectl' + ' ' + command,
            'get rs': 'kubectl' + ' ' + command,
            'version': 'kubectl' + ' ' + command,
            'cluster-info': 'kubectl' + ' ' + command,
            'config view': 'kubectl' + ' ' + command
        }.get(command, "")

def tf_command_helper_sys(cmd):
    """
    K8S_Shell_Driver Package mpw
    mpw v0.7
    Kubernetes Command Helper - sends shell scripts to Shell
    Works at Linux command line or Powershell
    Accepts filename and path and executes shell script
    as subprocess shell command
    :param cmd:
    :return:
    """
    print(cmd)
    try:
      retcode = subprocess.call([cmd], shell=True)
      if retcode < 0:
          print(sys.stderr, "Child was terminated by signal", -retcode)
      else:
          print(sys.stderr, "Child returned", retcode)
    except OSError as e:
          print(sys.stderr, "Execution failed:", e)

def tf_command_helper(cmd):
    """
    mpw v0.7
    Kubernetes Command Helper - sends non-executable
    shell commands to a command Shell
    Works at Linux command line or Powershell
    Accepts ankubectl run --image=nginx nginx-app --port=80 --env="DOMAIN=cluster"y non- OS executable command
    and sends it as subprocess shell command
    shell = True means this will routine handle
    :param cmd:
    :return:
    """
    print(cmd)
    try:
      retcode = subprocess.call([cmd], shell=True)
      if retcode < 0:
          print(sys.stderr, "Child was terminated by signal", -retcode)
      else:
          print(sys.stderr, "Child returned", retcode)
    except OSError as e:
        print(sys.stderr, "Execution failed:", e)

