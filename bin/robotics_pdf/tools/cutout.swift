import Foundation
import Vision
import CoreImage

let args = CommandLine.arguments
let inPath = args[1], outBase = args[2]
guard let ciImage = CIImage(contentsOf: URL(fileURLWithPath: inPath)) else { fatalError("cannot read \(inPath)") }
let handler = VNImageRequestHandler(ciImage: ciImage, options: [:])
let request = VNGenerateForegroundInstanceMaskRequest()
try handler.perform([request])
guard let result = request.results?.first else { fatalError("no foreground found") }
let ctx = CIContext()
let cs = CGColorSpace(name: CGColorSpace.sRGB)!
func write(_ buf: CVPixelBuffer, _ path: String) throws {
    try ctx.writePNGRepresentation(of: CIImage(cvPixelBuffer: buf), to: URL(fileURLWithPath: path), format: .RGBA8, colorSpace: cs, options: [:])
}
print("instances:", result.allInstances.count)
for inst in result.allInstances {
    let buf = try result.generateMaskedImage(ofInstances: [inst], from: handler, croppedToInstancesExtent: false)
    try write(buf, "\(outBase)-inst\(inst).png")
}
let all = try result.generateMaskedImage(ofInstances: result.allInstances, from: handler, croppedToInstancesExtent: false)
try write(all, "\(outBase)-all.png")

// Usage: swiftc -O cutout.swift -o cutout && ./cutout <in.jpg> <out-base>
// Writes <out-base>-inst<N>.png per foreground instance and <out-base>-all.png.
// frames/duck-standing-cutout.png = this on frames/duck-stands-free-16.5s.jpg,
// trimmed, then the socks erased (alpha := 0) in PIL over the rectangles
// (0,280,150,518) (150,352,172,518) (441,280,570,518) (420,352,441,518) of the
// trimmed+12px-bordered image, re-trimmed and re-bordered 12px. 2026-09-16.
