import re

LOG_PATTERN = re.compile(r'"\s+\d{3}\s+(-|\d+)(?:\s+(-|\d+))?')


def read_lines_in_chunks(file_path, chunk_size=1024 * 64):

    with open(file_path, 'r', encoding='utf-8') as f:
        buffer = ''
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                if buffer:
                    yield buffer
                break

            buffer += chunk
            lines = buffer.split('\n')

            buffer = lines.pop()

            for line in lines:
                yield line


def extract_bytes(line):

    match = LOG_PATTERN.search(line)
    if match:
        sent_str = match.group(1)
        received_str = match.group(2)

        sent = int(sent_str) if sent_str and sent_str != '-' else 0
        received = int(received_str) if received_str and received_str != '-' else 0

        return sent, received
    return 0, 0


def process_log(file_path):

    lines_gen = read_lines_in_chunks(file_path)

    bytes_gen = (extract_bytes(line) for line in lines_gen if line.strip())

    total_sent = 0
    total_received = 0

    for sent, received in bytes_gen:
        total_sent += sent
        total_received += received

    return total_sent, total_received


if __name__ == '__main__':

    log_file = '2017_05_07_nginx.txt'
    try:
        sent, received = process_log(log_file)
        print(f"Сумарно надіслано байтів: {sent}")
        print(f"Сумарно прийнято байтів: {received}")
    except FileNotFoundError:
        print(f"Файл {log_file} не знайдено.")