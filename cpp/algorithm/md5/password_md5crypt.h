#ifndef PASSWORD_MD5CRYPT_H
#define PASSWORD_MD5CRYPT_H
#include <string>

#define	MD5_RESULTLEN (128/8)

struct md5_context {
	unsigned long lo, hi;
	unsigned long a, b, c, d;
	unsigned char buffer[64];
	unsigned long block[MD5_RESULTLEN];
};

void safe_memset(void *data, int c, size_t size);

void md5_init(struct md5_context *ctx);
void md5_update(struct md5_context *ctx, const void *data, size_t size);
void md5_final(struct md5_context *ctx, unsigned char result[MD5_RESULTLEN]);
void md5_get_digest(const void *data, size_t size,
		    unsigned char result[MD5_RESULTLEN]);

bool Md5_salt(const std::string& password, std::string& md5_pass);

/*****************************************************************
����ԭ��:bool password_generate_md5_crypt(const char *pw, const char *salt, char *md5pass)
��������:����pw��salt����MD5pw
����˵��:pw:�û����������(δ����);salt:md5 salt;md5pass:(����)���ܺ������
����ֵ	:���ɳɹ�����true,���򷵻�false
*****************************************************************/
bool password_generate_md5_crypt(const char *pw, const char *salt, char *md5pass);

/*****************************************************************
����ԭ��:bool generate_salt(unsigned len, char *ret_salt)
��������:����md5��salt
����˵��:len:salt�ĳ���;ret_salt:(����)���ɵ�salt
����ֵ	:���ɳɹ�����true,���򷵻�false
*****************************************************************/
bool generate_salt(unsigned len, char *ret_salt);

/*****************************************************************
����ԭ��:bool generate_md5_password(const char *pw, char *md5pass)
��������:������֤
����˵��:pw:�û����������(δ����);md5pass:(����)���ɵ�md5����
����ֵ	:����ƥ�䷵��true,���򷵻�false
*****************************************************************/
bool generate_md5_password(const char *pw, char *md5pass);

/*****************************************************************
����ԭ��:bool check_password(const char *inputpw, const char *dbpw)
��������:������֤
����˵��:inputpw:�û����������(δ����);dbpw:���ݿ��в�ѯ����������(�Ѽ���)
����ֵ	:����ƥ�䷵��true,���򷵻�false
*****************************************************************/
bool check_password(const char *inputpw, const char *dbpw);

// std::string password,password_md5;
// Md5_salt(password, password_md5);

#endif
