static std::string charset = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
std::string Base10To62(size_t base10)
{
	std::string  result;
	do
	{
		result.push_back(charset[base10 % 62]);
		base10 /= 62;
	} while (base10);

	reverse(result.begin(), result.end());
	return result;
}

size_t Base62To10(const std::string & base62)
{
	size_t base10 = 0;

	for (size_t i = 0; i < base62.length(); i++)
	{
		const size_t index = charset.find(base62[i]);
		assert(index != std::string::npos);
		base10 = base10 * 62 + index;
	}

	return base10;
}