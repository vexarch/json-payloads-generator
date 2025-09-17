# json-payloads-generator

A Python class for generating unique JSON payloads to use in back-end server API testing.

## Features
- Uses only standard library modules for easy integration without extra dependencies.
- Inline comments for nearly every function for better IDE suggestions.
- Wide range of value generators.
- Supports external data (file-based rules) for realistic payload generation.
- Custom rule support: write your own rules.

## Usage
See [Documentation](./json_generator_docs.md) for details and examples.

## Third-Party Content Notice

This project includes `usernames.txt` and `passwords.txt` files sourced from the [SecLists](https://github.com/danielmiessler/SecLists) project.  
SecLists is licensed under the MIT License.  
Please see the [SecLists LICENSE](https://github.com/danielmiessler/SecLists/blob/master/LICENSE.txt) for details and attribution.

## Contributing

Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/my-feature`).
3. Commit your changes.
4. Push to your branch.
5. Open a pull request.

## Known Issues
- Syntax for some built-in rules can be complex.

## License

This project is licensed under the MIT License. See [LICENSE](./LICENSE) for details.