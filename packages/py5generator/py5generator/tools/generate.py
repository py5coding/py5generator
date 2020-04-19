import py5generator


def generate():
    py5generator.generate_py5()


def main():
    print('generating py5 library...')
    generate()
    print('done!')


if __name__ == '__main__':
    main()
