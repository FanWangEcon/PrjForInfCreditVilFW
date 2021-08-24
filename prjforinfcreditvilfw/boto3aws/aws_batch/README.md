# AWS Batch with Container

[AWS Guide: What is Batch?](https://docs.aws.amazon.com/batch/latest/userguide/what-is-batch.html)

AWS Batch, given jobs submitted to it, determines optimally how much computing
resources to provide.
> AWS Batch will efficiently launch, manage, and terminate EC2 instances as needed

## Price of AWS Batch with Spot Instances?

AWS Batch does not add costs. Costs are based on instances used. If one uses EC2 spot instances, one could
specify the price one is willing to pay. Based on supply and demand of EC2 instances, EC2 become available if price goes
below one's bid level. Spot instances requires potential waiting time, and could potentially
be terminated when capacity is no longer available due to high demand for on-demand instances.

Since November 2017--[Streamlined Access to Spot Capacity](https://aws.amazon.com/blogs/aws/amazon-ec2-update-streamlined-access-to-spot-capacity-smooth-price-changes-instance-hibernation/)
, one no longer needs to specify maximum price willing to pay for spot instances. It is be default 100 percent
of on demand instance prices. But one pays lower price if demand supply for excess capacity takes price below
100 percent for spot vs on-demand EC2 instances.

Spot instances could potentially be terminated by AWS if demand for on-demand too high.
On-demand instances are safer to run.

## Keeping a persistent EC2 instance?

When specifying compute environment for batch, if one sets minimal vcpu requirement to
more than 0, then there will always be a EC2 instance running that has that required
level of cpu. After a compute environment with more than 0 vcpu is specified, in the EC2
console, a EC2 instance will start up that satisfies the minimum vcpu requirement. If this is set to 0,
EC2 instances would start up based on batch job needs, and would be terminated when your batch jobs are done.
 See: [Using min CPU=2 but get m4.16xlarge](https://forums.aws.amazon.com/thread.jspa?messageID=809896)

## How to run many Batch jobs together?

Under compute specification for batch job, if one sets a low number for maximum vcpu,
then batch jobs would wait in queue if the total cpu requirements for all waiting jobs exceed
the maximum vcpu level. If one wants AWS batch to automatically scale EC2 instances based on
the number of jobs submitted, then set a very large number for vcpu. See:
[https://forums.aws.amazon.com/thread.jspa?messageID=765721&#765721](https://forums.aws.amazon.com/thread.jspa?messageID=765721&#765721)


## Batch Array

Batch array re-runs the same instance many times, great for simulation, trying out model at different parameters.
