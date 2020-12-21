import json
import os
import hashlib
BLOCKCHAIN_DIR = 'blockchain/'

def get_hash(prev_block):
    with open(BLOCKCHAIN_DIR + prev_block, 'rb') as f:
        content = f.read()
    return hashlib.md5(content).hexdigest()


def check_integrity():
    files = sorted(os.listdir(BLOCKCHAIN_DIR), key=lambda x: int(x))

    results = []

    for file in files[1:]:
        with open(BLOCKCHAIN_DIR + file) as f:
            block = json.load(f)

        prev_hash = block.get('prev_block').get('hash')
        prev_filename = block.get('prev_block').get('filename')
        actual_hash = get_hash(prev_filename)
        if prev_hash == actual_hash:
            res = 'OK'
        else:
            res = 'Was Changed'
        print(f"Block {prev_filename}: {res}")
        results.append({'block': prev_filename, 'result': res})
    return results


def write_block(lendee, lender, amount):
    blocks_count = len(os.listdir(BLOCKCHAIN_DIR))
    prev_block = str(blocks_count)
    data = {
        "lendee": lendee,
        "lender": lender,
        "amount": amount,
        "prev_block": {
            "hash": get_hash(prev_block),
            "filename": str(blocks_count)
        }
    }

    current_block = BLOCKCHAIN_DIR + str(blocks_count + 1)

    with open(current_block, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        f.write('\n')

def main():
    check_integrity()
    # write_block(lendee="Jane", lender="Allan", amount=2750)

if __name__ == '__main__':
    main()