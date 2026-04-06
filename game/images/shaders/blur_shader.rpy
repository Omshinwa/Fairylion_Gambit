## Blur shaders — mipmap LOD technique (same as Ren'Py's built-in blur)
##
## How it works:
##   Each mipmap LOD level is the texture at half the previous resolution.
##   Sampling at LOD i ≈ sampling a version blurred to radius 2^i pixels.
##   A Gaussian weighting over LOD levels 0–13 gives smooth isotropic blur
##   in ~13 texture samples, independent of blur strength.
##
## gl_mipmap True generates the mipmap chain for the transformed displayable.
##
## Transforms:
##   gaussian_blur(sigma)
##   partial_blur(sigma, x1, y1, x2, y2, softness)
##   blur_masked(sigma, mask)
##
## sigma — blur radius in pixels (converted to log2 inside the shader)
##   sigma=2  → subtle,  sigma=8  → medium,  sigma=32 → heavy

init python:

    # shared GLSL function — Gaussian-weighted mipmap sample
    # u_sigma: blur radius in pixels
    FAIRYLION_BLUR_FN = """
vec4 fl_lod_blur(sampler2D tex, vec2 uv, float sigma) {
    float lod    = log2(max(sigma, 1.0));
    vec4  colour = vec4(0.0);
    float norm   = 0.0;

    // LODs -5..0 all collapse to LOD 0 (can't go below full-res)
    float base_w = 0.0;
    for (float i = -5.0; i < 1.0; i += 1.0) {
        base_w += exp(-0.5 * pow(lod - i, 2.0));
    }
    colour += base_w * texture2D(tex, uv, 0.0);
    norm   += base_w;

    // LODs 1..13
    for (float i = 1.0; i < 14.0; i += 1.0) {
        if (i >= lod + 5.0) break;
        float w = exp(-0.5 * pow(lod - i, 2.0));
        colour += w * texture2D(tex, uv, i);
        norm   += w;
    }

    return (norm > 0.0) ? colour / norm : texture2D(tex, uv, 0.0);
}
    """

    # ── image-masked blur ─────────────────────────────────────────────────────
    ## mask red channel: 1.0 = full blur, 0.0 = original

    renpy.register_shader("fairylion.masked_blur",
        variables="""
uniform sampler2D tex0;
uniform sampler2D u_mask;
varying vec2      v_tex_coord;
uniform float     u_sigma;
        """,
        fragment_functions=FAIRYLION_BLUR_FN,
        fragment_300="""
vec2  uv    = v_tex_coord;
float blend = texture2D(u_mask, uv).r;

gl_FragColor = mix(
    texture2D(tex0, uv, 0.0),
    fl_lod_blur(tex0, uv, u_sigma),
    blend
);
        """)

transform blur_masked(sigma=8.0, mask=""):
    mesh True
    gl_mipmap True
    shader "fairylion.masked_blur"
    u_sigma float(sigma)
    u_mask  mask
