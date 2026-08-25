const std = @import("std");

pub const RenderMode = union(enum) {
    software,
    hardware: u32,
    headless,
};

pub const Vertex = packed struct {
    x: f32,
    y: f32,
    z: f32,
};

pub const EngineConfig = struct {
    title: []const u8,
    width: u32 = 800,
    height: u32 = 600,
    mode: RenderMode = .software,
};

pub const Engine = struct {
    allocator: std.mem.Allocator,
    config: EngineConfig,
    vertices: std.ArrayList(Vertex),

    pub fn init(allocator: std.mem.Allocator, config: EngineConfig) !Engine {
        var list = std.ArrayList(Vertex).init(allocator);
        errdefer list.deinit();

        return Engine{
            .allocator = allocator,
            .config = config,
            .vertices = list,
        };
    }

    pub fn deinit(self: *Engine) void {
        self.vertices.deinit();
    }

    pub fn add_vertex(self: *Engine, v: Vertex) !void {
        try self.vertices.append(v);
    }

    pub fn compute_simd_normals(a: @Vector(4, f32), b: @Vector(4, f32)) @Vector(4, f32) {
        return a * b;
    }
};

pub fn Container(comptime T: type) type {
    return struct {
        item: T,
        pub fn get(self: @This()) T {
            return self.item;
        }
    };
}
