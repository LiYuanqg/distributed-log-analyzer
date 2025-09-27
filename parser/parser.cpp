#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>

struct LogEntry {
    std::string timestamp;
    std::string type;
    std::string node;
    std::string message;
};

// Function to trim whitespace
std::string trim(const std::string &str) {
    size_t first = str.find_first_not_of(" \t\n");
    size_t last = str.find_last_not_of(" \t\n");
    if (first == std::string::npos) return "";
    return str.substr(first, (last - first + 1));
}

// Parse a single log line into LogEntry
LogEntry parseLine(const std::string &line) {
    LogEntry entry;
    // Expected log format:
    // [2025-09-27 10:01:23] ALARM Node 3 Disk failed
    size_t time_start = line.find('[');
    size_t time_end = line.find(']');
    if (time_start == std::string::npos || time_end == std::string::npos) {
        entry.timestamp = "";
        entry.type = "UNKNOWN";
        entry.node = "";
        entry.message = line;
        return entry;
    }

    entry.timestamp = line.substr(time_start + 1, time_end - time_start - 1);

    std::string rest = line.substr(time_end + 1);
    std::istringstream iss(rest);
    iss >> entry.type >> entry.node;
    std::getline(iss, entry.message);
    entry.message = trim(entry.message);

    return entry;
}

// Write parsed logs to CSV
void writeCSV(const std::vector<LogEntry> &logs, const std::string &outfile) {
    std::ofstream out(outfile);
    out << "Timestamp,Type,Node,Message\n";
    for (const auto &entry : logs) {
        out << "\"" << entry.timestamp << "\","
            << "\"" << entry.type << "\","
            << "\"" << entry.node << "\","
            << "\"" << entry.message << "\"\n";
    }
    out.close();
}

int main() {
    std::string logFile = "logs/sample.log";
    std::string outputFile = "data/parsed_logs.csv";

    std::ifstream infile(logFile);
    if (!infile.is_open()) {
        std::cerr << "Failed to open log file: " << logFile << std::endl;
        return 1;
    }

    std::vector<LogEntry> logs;
    std::string line;
    while (std::getline(infile, line)) {
        if (line.empty()) continue;
        LogEntry entry = parseLine(line);
        logs.push_back(entry);
    }
    infile.close();

    writeCSV(logs, outputFile);
    std::cout << "Parsed " << logs.size() << " log entries. Output: " << outputFile << std::endl;

    return 0;
}
