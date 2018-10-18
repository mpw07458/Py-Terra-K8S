import os
import shutil
import subprocess
import sys
import uuid


class AKSTerraform:
    def __init__(self, tf_source_manifest_path, tf_storage_account, tf_storage_container, tf_aks_variables=None):
        aks_k8s_env()
        self.aks_name = os.path.basename(tf_source_manifest_path).split(".")[0]
        self.aks_object_id = str(uuid.uuid4())
        self.tf_source_manifest_path = tf_source_manifest_path
        print(self.tf_source_manifest_path)
        self.tf_tmpdir = os.path.join(".", "." + self.aks_object_id)
        print(self.tf_tmpdir)
        self.tf_manifestdir = os.path.join(self.tf_tmpdir, self.aks_name)
        print(self.tf_manifestdir)
        self.tf_state_path = os.path.join(self.tf_manifestdir, "terraform.tfstate")
        print(self.tf_state_path)
        self.AKS_State_str = self.set_aks_state(tf_storage_account, tf_storage_container)
        self.AKS_Plan_str = self.set_aks_plan("/out.plan")
        self.AKS_Apply_str = self.set_aks_apply("/out.plan")
        self.variables = ""
        self.copy_tmp_manifest()
        self.variables = self.tf_variable_parse(tf_aks_variables)
        print("Variables: ", tf_aks_variables)
        self.gen_tf_vars_file()
        init(self)
        plan(self)
        apply(self)
        self.aks_cleanup()
        aks_k8s_config()
        helm_config()
        return

    def aks_cleanup(self):
        self.remove_tmp_manifest()

    @staticmethod
    def is_a_terraform_file(f):
        return os.path.isfile(f) and (f.lower().endswith(".tf") or f.lower().endswith(".tf.json"))

    def copy_tmp_manifest(self):
        if os.path.isdir(self.tf_source_manifest_path):
            files = [f for f in os.listdir(self.tf_source_manifest_path)
                     if self.is_a_terraform_file(os.path.join(self.tf_source_manifest_path, f))]
            if len(files) > 0:
                if not os.path.isdir(self.tf_tmpdir):
                    os.mkdir(self.tf_tmpdir)
                shutil.copytree(self.tf_source_manifest_path, os.path.join(self.tf_tmpdir, self.aks_name))
            else:
                raise (Exception("Terraform files not found.  Must have at least "
                                 "one *.tf or *.tf.json file to feed to Terraform."))
        elif self.is_a_terraform_file(self.tf_source_manifest_path):
            if not os.path.isdir(self.tf_tmpdir):
                os.mkdir(self.tf_tmpdir)
            if not os.path.isdir(self.tf_manifestdir):
                os.mkdir(self.tf_manifestdir)
            shutil.copy(self.tf_source_manifest_path, self.tf_manifestdir)
        else:
            raise (Exception("Manifest file not found.  Must have a *.tf or *.tf.json file to feed to Terraform."))

    def gen_tf_vars_file(self):
        with open(os.path.join(self.tf_manifestdir, 'variables.tf'), 'w') as vars_file:
            vars_file.write(self.variables)
        vars_file.close()

    def remove_tmp_manifest(self):
        if os.path.isdir(self.tf_tmpdir):
            shutil.rmtree(self.tf_tmpdir)

    @staticmethod
    def set_aks_state(storageaccount, storagecontainer):
        account_str = "-backend-config=" + "'" + "storage_account_name=" + storageaccount + "'"
        container_str = "-backend-config=" + "'" + "container_name=" + storagecontainer + "'"
        return account_str + " " + container_str

    def set_aks_plan(self, plan_str):
        aks_plan_str = "-out " + self.tf_manifestdir + plan_str
        return aks_plan_str

    def set_aks_apply(self, apply_str):
        aks_apply_str = self.tf_manifestdir + apply_str
        return aks_apply_str

    @staticmethod
    def tf_variable_parse(variables):
        if variables is not None:
            tf_vars = ""
            for variable in variables:
                innervar = variables[variable]
                print(variable, innervar)
                if isinstance(innervar, int):
                    tf_vars = tf_vars + "variable \"" + variable + "\" " + "{" + "\n" + "  default = " \
                              + str(innervar) + "\n" + "}" + "\n" + "\n"
                else:
                    tf_vars = tf_vars + "variable \"" + variable + "\" " + "{" + "\n" + "  default = " \
                              + "\"" + innervar + "\"" + "\n" + "}" + "\n" + "\n"
            return tf_vars
        else:
            return None


def aks_k8s_env():
    sh_cmd = "source env-Inno.sh"
    print(sh_cmd)
    tf_command_helper_sys(sh_cmd)


def init(self):
    tf_cmd = "Terraform init" + " " + self.AKS_State_str + " " + self.tf_manifestdir
    print(tf_cmd)
    tf_command_helper(tf_cmd)


def plan(self):
    tf_cmd = "Terraform plan" + " " + self.AKS_Plan_str + " " + self.tf_manifestdir
    print(tf_cmd)
    tf_command_helper(tf_cmd)


def apply(self):
    tf_cmd = "Terraform apply" + " " + self.AKS_Apply_str
    print(tf_cmd)
    tf_command_helper(tf_cmd)

def helm_config():
    """
    configure helm
    :return:
    """
    sh_cmd = "kubectl create -f helm/tiller-rbac.yaml"
    print(sh_cmd)
    tf_command_helper_sys(sh_cmd)
    sh_cmd = "helm-init.sh"
    print(sh_cmd)
    tf_command_helper_sys(sh_cmd)
    return

def aks_k8s_config():
    """
    configure aks k8s kubeconfig
    :return:
    """
    sh_cmd = "echo "'$(terraform output kube_config)'" > OpenInnok8s"
    print(sh_cmd)
    tf_command_helper_sys(sh_cmd)
    sh_cmd = "mkdir ~/.kube/config"
    print(sh_cmd)
    tf_command_helper_sys(sh_cmd)
    sh_cmd = "cp -p /Users/michaelwilliams/Documents/GitHub/Py-Terra-K8S/Py-Terra-K8S/OpenInnok8s ~/.kube/config/."
    print(sh_cmd)
    tf_command_helper_sys(sh_cmd)
    sh_cmd = "export KUBECONFIG=~/.kube/config/OpenInnok8s"
    print(sh_cmd)
    tf_command_helper_sys(sh_cmd)
    return


def tf_command_helper_sys(cmd):
    """
    Terraform Command Helper - sends shell scripts to Shell
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
    Terraform Command Helper -  sends non-executable
    shell commands to a command Shell
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
