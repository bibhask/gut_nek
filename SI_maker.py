def generate_geo_file(filename="y_2.geo"):
    # AspectRatio
    gamma = 2.0125
    p = 8

    c1 = (gamma - (p*0.0125) )/(p-1)
    print(f"crypt = {c1}")

    k = c1/(0.0125)
    print(f"\chi = {k}")
   # c1 = 0.654167# size of crypt
    c2 = 0.01250  # size of villi
    Q = (gamma -c1)/(c1+c2)

    N = int(Q) + 1
    print(f"Number of villi = {N}")

    #N = 120
    L = 4 * N
    T = L + 5
    J = T - 3
    
    c3 = 0.9     # villi height
    c5 = 0       # radius

    # Transfinite commands
    t1 = 2
    # t2 = 4*gamma
    # t3 = gamma + 4
    # t5 = 4
    #t2 = 160
    #t3 = 160
    t5 = 4
    K = 20
    P = 2*N + 1
    z_value = 0
    weight = 1.0

    with open(filename, "w") as file:
        file.write("SetFactory(\"OpenCASCADE\");\n")
        file.write("//+\n")

        file.write("Point(1) = {0.0, 0.0, 0, 1.0};\n")
        file.write("//+\n")

        file.write(f"Point(2) = {{0.0, {c3}, 0, 1.0}};\n")
        file.write("//+\n")

        point_index = 3

        # points
        for i in range(1, N+1):
            file.write(
                f"Point({point_index}) = {{{i*c2 + (i-1)*c1}, {c3}, {z_value}, {weight}}};\n"
            )
            file.write("//+\n")
            point_index += 1

            file.write(
                f"Point({point_index}) = {{{i*c2 + (i-1)*c1}, 1.0, {z_value}, {weight}}};\n"
            )
            file.write("//+\n")
            point_index += 1

            file.write(
                f"Point({point_index}) = {{{i*c2 + i*c1}, 1.0, {z_value}, {weight}}};\n"
            )
            file.write("//+\n")
            point_index += 1

            file.write(
                f"Point({point_index}) = {{{i*c2 + i*c1}, {c3}, {z_value}, {weight}}};\n"
            )
            file.write("//+\n")
            point_index += 1

        file.write(f"Point({point_index}) = {{{gamma}, {c3}, {z_value}, {weight}}};\n")
        file.write("//+\n")
        point_index += 1

        file.write(f"Point({point_index}) = {{{gamma}, 0.0, {z_value}, {weight}}};\n")
        file.write("//+\n")
        point_index += 1

        file.write(f"Point({point_index}) = {{{N*(c1+c2)}, 0.0, {z_value}, {weight}}};\n")
        file.write("//+\n")
        point_index += 1

        # LINE_COMMANDS_PRIMARY_LINES
        file.write(f"Line(1) = {{1, {T}}};\n")
        file.write("//+\n")
        file.write(f"Transfinite Curve {{1}} = {P} Using Progression 1;\n")
        file.write("//+\n")
        file.write(f"Physical Curve(\"axis\", {T+4}) = {{1}};\n")
        file.write("//+\n")

        file.write(f"Line(2) = {{{T}, {T-1}}};\n")
        file.write("//+\n")
        file.write(f"Transfinite Curve {{2}} = {2} Using Progression 1;\n")
        file.write("//+\n")
        file.write(f"Physical Curve(\"axis\", {T+4}) += {{2}};\n")
        file.write("//+\n")

        file.write(f"Line(3) = {{{T-1}, {T-2}}};\n")
        file.write("//+\n")
        file.write(f"Transfinite Curve {{3}} = {K} Using Progression 1;\n")
        file.write("//+\n")
        file.write(f"Physical Curve(\"outlet\", {T+5}) = {{3}};\n")
        file.write("//+\n")

        file.write(f"Line(4) = {{{T-2}, {T-3}}};\n")
        file.write("//+\n")
        file.write(f"Transfinite Curve {{4}} = {2} Using Progression 1;\n")
        file.write("//+\n")
        file.write(f"Physical Curve(\"skin\", {T+6}) = {{4}};\n")
        file.write("//+\n")

        line_index = 5

        for i in range(L):
            file.write(f"Line({line_index}) = {{{J-i}, {J-(i+1)}}};\n")
            file.write("//+\n")
            file.write(f"Transfinite Curve {{{line_index}}} = {t1} Using Progression 1;\n")
            file.write("//+\n")
            file.write(f"Physical Curve(\"skin\", {T+7}) += {{{line_index}}};\n")
            file.write("//+\n")
            line_index += 1

        file.write(f"Line({line_index}) = {{2, 1}};\n")
        file.write("//+\n")
        file.write(f"Transfinite Curve {{{line_index}}} = {K} Using Progression 1;\n")
        file.write("//+\n")
        file.write(f"Physical Curve(\"inlet\", {T+7}) = {{{line_index}}};\n")
        file.write("//+\n")
        line_index += 1

        # INTERNAL_LINES
        for i in range(N):
            file.write(f"Line({line_index}) = {{{3+4*i}, {(3+4*i)+3}}};\n")
            file.write("//+\n")
            file.write(f"Transfinite Curve {{{line_index}}} = {t1} Using Progression 1;\n")
            file.write("//+\n")
            line_index += 1

        file.write(f"Line({line_index}) = {{{J}, {T}}};\n")
        file.write("//+\n")
        file.write(f"Transfinite Curve {{{line_index}}} = {K} Using Progression 1;\n")
        file.write("//+\n")
        line_index += 1

        # body
        surface_index = 1

        ids = [T, 1, -(T + N + 1)]
        for i in range(N):
            ids.append(-(T + N - i))
            ids.append(8 + 4 * i)

        file.write(f"Curve Loop({surface_index}) = {{{', '.join(map(str, ids))}}};\n")
        file.write("//+\n")
        file.write(f"Plane Surface({surface_index}) = {{{surface_index}}};\n")
        file.write("//+\n")
        file.write(f"Transfinite Surface {{{surface_index}}} = {{1, {T}, {J}, 2}};\n")
        file.write("//+\n")
        file.write(f"Recombine Surface {{{surface_index}}};\n")
        file.write("//+\n")
        file.write(f"Physical Surface(\"chyme\", {T+8}) = {{{surface_index}}};\n")
        file.write("//+\n")
        surface_index += 1

        loop2 = [4, (T + N + 1), 2, 3]
        file.write(f"Curve Loop({surface_index}) = {{{', '.join(map(str, loop2))}}};\n")
        file.write("//+\n")
        file.write(f"Plane Surface({surface_index}) = {{{surface_index}}};\n")
        file.write("//+\n")
        file.write(f"Transfinite Surface {{{surface_index}}} = {{{T}, {T-1}, {T-2}, {J}}};\n")
        file.write("//+\n")
        file.write(f"Recombine Surface {{{surface_index}}};\n")
        file.write("//+\n")
        file.write(f"Physical Surface(\"chyme\", {T+8}) += {{{surface_index}}};\n")
        file.write("//+\n")
        surface_index += 1

        for i in range(N):
            loopi = [(T + N - i), (5 + 4*i), (6 + 4*i), (7 + 4*i)]
            file.write(f"Curve Loop({surface_index}) = {{{', '.join(map(str, loopi))}}};\n")
            file.write("//+\n")
            file.write(f"Plane Surface({surface_index}) = {{{surface_index}}};\n")
            file.write("//+\n")
            file.write(
                f"Transfinite Surface {{{surface_index}}} = "
                f"{{{J-3-4*i}, {J-4*i}, {J-1-4*i}, {J-2-4*i}}};\n"
            )
            file.write("//+\n")
            file.write(f"Recombine Surface {{{surface_index}}};\n")
            file.write("//+\n")
            file.write(f"Physical Surface(\"chyme\", {T+8}) += {{{surface_index}}};\n")
            file.write("//+\n")
            surface_index += 1

    print(f"Geometry has been written to {filename} file. Open it in GMSH")


if __name__ == "__main__":
    generate_geo_file()
