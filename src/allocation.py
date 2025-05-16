def allocate_objects(policy, profile):
    """
    Given a policy and a profile this function allocate objects to agents
    """
    allocation = []
    available_objects = set(range(1, len(profile[0]) + 1))

    for i, k in enumerate(policy):
        agent_pref = profile[i]
        agent_allocation = []

        for obj in agent_pref:

            if len(agent_allocation) < k and obj in available_objects:
                agent_allocation.append(obj)
                available_objects.remove(obj)

        allocation.append(agent_allocation)
    
    return allocation


# Test
# from generate_policies import generate_policy
# from generate_IC_profiles import sample_k_IC_profiles
# n = 10
# m = 20
# all_policies = generate_policy(n,m)
# for _ in range(200000): next(all_policies) # To have an interesting policy
# policy = next(all_policies)
# profile = sample_k_IC_profiles(1,n,m)[0]
# print(profile)
# allocation = allocate_objects(policy, profile)
# print(allocation)