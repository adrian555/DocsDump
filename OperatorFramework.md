### summary

* explored Openshift through minishift on ubuntu and centos VMs
* deployed and run FfDL service on minishift, blogged on medium.com
* investigated opendatahub.io for Red Hat's data and AI platform strategy
* dug into Operator Framework open source project, especially the Operator SDK, Operator Lifecycle Manager and Operator Registry parts
* created Ansible and Helm types of operators with Operator SDK
* created FfDL, Kubeflow Pipeline, Kubeflow base, Jupyterlab, Pachyderm and OpenAIHub operators
* pushed FfDL operator to operatorhub.io
* built operator CSV bundle images and ran with local operator registry server
* created CatalogSource using local registry server for OLM to discover all operators
* deployed operators and services in catalog through OLM
* created openaihub Python package to integrate these work and install OpenAIHub platform with one command


### details

Given that no [Openshift](www.openshift.com) clusters had been granted for me to use, I had started by setting up clusters running Openshift Container Platform 3.11 through installing [minishift](https://github.com/minishift/minishift) on ubuntu and centos VMs. Then explored the added values brought by [OKD](https://www.okd.io/) compared with other Kubernetes clusters. The first experiment was to deploy FfDL service on minishift. It took some time to get the correct cluster permission and work around known issues to current Openshift project. Finally the FfDL could be run on the minishift and a tutorial was published to [medium.com](https://medium.com/@dsml4real/deep-learning-model-training-with-ffdl-on-minishift-510dc40fca56).


Next we researched [opendatahub.io](https://opendatahub.io/) to peek into Red Hat's strategy for data and AI platform. Learned and tried [ansible](https://www.ansible.com/) and [ansible playbook bundle](https://github.com/ansibleplaybookbundle/ansible-playbook-bundle), the Red Hat's approach to package and install applications on Openshift clusters. We were able to deploy the whole package and tried some examples.


Open source project [Operator Framework](https://github.com/operator-framework) became my focus after Opeshift Common summit. Immersed in knowledge of [Operator SDK](https://github.com/operator-framework/operator-sdk), [Operator Lifecycle Manager](https://github.com/operator-framework/operator-lifecycle-manager) (OLM) and [Operator Registry](https://github.com/operator-framework/operator-registry), started to create operators for OpenAIHub project, then deployed them manually and through OLM. So far six operators had been created. These operators are FfDL (already pushed to [operatorhub.io](https://operatorhub.io/)), Kubeflow Pipeline, Kubeflow base, Jupyterlab, Pachyderm and OpenAIHub. 
Each is either an Ansible or Helm type of operator. Each can be installed on IKS and OKD clusters. Some operators have problem with the Openshift cluster on IBM Cloud and we are looking at solutions. 

With [OpenAIHub](https://github.ibm.com/OpenAIHub/openaihub) project, we made decision to adopt OLM and depend on it to install the services. Created and spawned a local operator registry server. All these operators are registered to the server. CatalogSource is created to use this local registry and so all operators can be discovered by OLM. [openaihub](https://pypi.org/project/openaihub/) Python package is created to deploy a minimal set of operators for OpenAIHub and start the services.


During the course some limitation of OLM and Operator Registry were encountered. For example, is it possible to pass env values to an operator through OLM? Also, can the local registry server be enhanced to add new operator's CSV on the fly? I am working on possible solutions. Also looking at contributing experience back to Operator Framework community.


Finally, only until recently we were able to provision an Openshift 3.11 cluster from IBM Cloud. Lack of cloud infrastructure support is a pain point to us in the past and still, today, we do not have any Openshift 4.1 clusters. minishift will continue to run OKD 3.11 for a while. And [code-ready container](https://github.com/code-ready/crc), which is supposedly to provide Openshift 4.1 for open source community use, is actually depending on Red Hat internal bundle image. So we do not have test infrastructure to fully test and certify our work on Openshift 4.1 yet.
