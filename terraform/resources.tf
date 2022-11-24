locals {
    data = jsondecode(file("${path.module}/variables.json"))
    instances = {for instance in local.data.instances : instance.name => instance}
    security_groups = {for sg in local.data.security_groups : sg.name => sg}
    vpcs = {for vpc in local.data.vpcs : vpc.name => vpc}
    subnets = {for subnet in local.data.subnets : subnet.name => subnet}
    users = {for user in local.data.users : user.name => user}
}

resource "aws_instance" "instance_test" {
    for_each        = local.instances
    instance_type   = each.value.instance_type
    ami             = each.value.ami

    tags = {
        Name = each.value.name
    }
}