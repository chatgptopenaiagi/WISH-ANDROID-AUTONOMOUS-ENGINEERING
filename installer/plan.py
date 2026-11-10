"""Pure peak-space planning, including staging, extraction, rollback and reserve."""
GIB = 1024 ** 3
MIB = 1024 ** 2


def plan_install(*, free_storage, available_ram, download_bytes, unpacked_bytes, rollback_bytes,
                 reserve_bytes=10 * GIB, minimum_ram=768 * MIB):
    values = [free_storage, available_ram, download_bytes, unpacked_bytes, rollback_bytes, reserve_bytes, minimum_ram]
    if any(type(value) is not int or value < 0 for value in values):
        raise ValueError('Resource values must be nonnegative integer byte counts.')
    peak_required = reserve_bytes + download_bytes + unpacked_bytes + rollback_bytes
    failures = []
    if free_storage < peak_required:
        failures.append('insufficient_storage')
    if available_ram < minimum_ram:
        failures.append('insufficient_ram')
    return {'allowed_to_plan': not failures, 'failures': failures, 'peak_storage_required': peak_required,
            'remaining_after_peak': free_storage - (peak_required - reserve_bytes),
            'installs_software': False, 'downloads_software': False}
