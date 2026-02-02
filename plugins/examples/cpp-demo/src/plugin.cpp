/**
 * C++ Demo Plugin for ClipShot
 * 
 * This plugin demonstrates high-performance native plugin development
 * using C++ and pybind11.
 */

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <string>
#include <vector>
#include <map>
#include <atomic>
#include <iostream>

namespace py = pybind11;

/**
 * Plugin metadata
 */
struct PluginInfo {
    std::string id;
    std::string name;
    std::string version;
    
    PluginInfo(std::string id_, std::string name_, std::string version_)
        : id(std::move(id_)), name(std::move(name_)), version(std::move(version_)) {}
};

/**
 * Clip data structure
 */
struct Clip {
    std::string id;
    std::string title;
    uint32_t width;
    uint32_t height;
    
    Clip(std::string id_, std::string title_, uint32_t width_, uint32_t height_)
        : id(std::move(id_)), title(std::move(title_)), width(width_), height(height_) {}
};

/**
 * Main C++ Demo Plugin class
 */
class CppDemoPlugin {
private:
    PluginInfo info_;
    std::string config_;
    std::atomic<size_t> clip_count_;
    bool use_opencl_;

public:
    CppDemoPlugin()
        : info_("com.clipshot.cpp-demo", "C++ Demo Plugin", "1.0.0"),
          config_(""),
          clip_count_(0),
          use_opencl_(false) {}

    /**
     * Initialize the plugin
     */
    void init(const std::string& config) {
        config_ = config;
        
        std::cout << "⚡ C++ Demo Plugin initialized!" << std::endl;
        std::cout << "   ID: " << info_.id << std::endl;
        std::cout << "   Version: " << info_.version << std::endl;
        std::cout << "   OpenCL: " << (use_opencl_ ? "enabled" : "disabled") << std::endl;
    }

    /**
     * Shutdown the plugin
     */
    void shutdown() {
        size_t count = clip_count_.load();
        std::cout << "👋 C++ Demo Plugin shutting down" << std::endl;
        std::cout << "   Total clips processed: " << count << std::endl;
    }

    /**
     * Handle clip captured event
     */
    void on_clip_captured(const Clip& clip) {
        clip_count_++;
        size_t count = clip_count_.load();
        
        std::cout << "🎬 Clip captured (C++): " << clip.title << std::endl;
        std::cout << "   ID: " << clip.id << std::endl;
        std::cout << "   Resolution: " << clip.width << "x" << clip.height << std::endl;
        std::cout << "   Total processed: " << count << std::endl;
    }

    /**
     * Get plugin status (custom API endpoint)
     */
    py::dict get_status() {
        py::dict status;
        status["status"] = "healthy";
        status["version"] = info_.version;
        status["clip_count"] = clip_count_.load();
        status["use_opencl"] = use_opencl_;
        status["language"] = "cpp";
        return status;
    }

    /**
     * Process video frame (demonstrates high-performance operation)
     */
    std::vector<uint8_t> process_frame(uint32_t width, uint32_t height, 
                                       const std::vector<uint8_t>& data) {
        std::cout << "🎞️  Processing frame: " << width << "x" << height 
                  << " (" << data.size() << " bytes)" << std::endl;
        
        std::vector<uint8_t> output = data;
        
        // Example: Apply a simple filter
        for (auto& pixel : output) {
            pixel = std::min(255, static_cast<int>(pixel) + 10);
        }
        
        std::cout << "   ✅ Frame processed" << std::endl;
        return output;
    }

    /**
     * Get statistics
     */
    py::dict get_stats() {
        py::dict stats;
        stats["clips_processed"] = clip_count_.load();
        stats["opencl_enabled"] = use_opencl_;
        return stats;
    }

    /**
     * Reset counters
     */
    size_t reset_counters() {
        size_t old_count = clip_count_.exchange(0);
        std::cout << "🔄 Counters reset! (was: " << old_count << ")" << std::endl;
        return old_count;
    }

    // Getters for plugin info
    const std::string& get_id() const { return info_.id; }
    const std::string& get_name() const { return info_.name; }
    const std::string& get_version() const { return info_.version; }
};

/**
 * pybind11 module definition
 */
PYBIND11_MODULE(cpp_demo_plugin, m) {
    m.doc() = "C++ Demo Plugin for ClipShot";

    // Bind PluginInfo
    py::class_<PluginInfo>(m, "PluginInfo")
        .def(py::init<std::string, std::string, std::string>())
        .def_readwrite("id", &PluginInfo::id)
        .def_readwrite("name", &PluginInfo::name)
        .def_readwrite("version", &PluginInfo::version);

    // Bind Clip
    py::class_<Clip>(m, "Clip")
        .def(py::init<std::string, std::string, uint32_t, uint32_t>())
        .def_readwrite("id", &Clip::id)
        .def_readwrite("title", &Clip::title)
        .def_readwrite("width", &Clip::width)
        .def_readwrite("height", &Clip::height);

    // Bind CppDemoPlugin
    py::class_<CppDemoPlugin>(m, "CppDemoPlugin")
        .def(py::init<>())
        .def("init", &CppDemoPlugin::init)
        .def("shutdown", &CppDemoPlugin::shutdown)
        .def("on_clip_captured", &CppDemoPlugin::on_clip_captured)
        .def("get_status", &CppDemoPlugin::get_status)
        .def("process_frame", &CppDemoPlugin::process_frame)
        .def("get_stats", &CppDemoPlugin::get_stats)
        .def("reset_counters", &CppDemoPlugin::reset_counters)
        .def_property_readonly("id", &CppDemoPlugin::get_id)
        .def_property_readonly("name", &CppDemoPlugin::get_name)
        .def_property_readonly("version", &CppDemoPlugin::get_version);

    m.attr("__version__") = "1.0.0";
}
