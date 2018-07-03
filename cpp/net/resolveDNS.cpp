 struct addrinfo hints;
  memset(&hints, 0, sizeof(hints));
  hints.ai_family = AF_UNSPEC; /* v4 or v6 is fine. */
  hints.ai_socktype = SOCK_STREAM;
  hints.ai_protocol = IPPROTO_TCP; /* We want a TCP socket */
  hints.ai_flags = AI_PASSIVE;    /* For wildcard IP address */

								  /* Look up the hostname. */
  struct addrinfo* answer = nullptr;
  int err = getaddrinfo("ipv6.baidu.com", nullptr, &hints, &answer);
 
	  for (struct addrinfo* rp = answer; rp != nullptr; rp = rp->ai_next) {
		  char buff[512] = { 0 };
		  void *ptr;
		  switch (rp->ai_family) {
		  case AF_INET:
			  ptr = &((struct sockaddr_in *) rp->ai_addr)->sin_addr;
			  break;
		  case AF_INET6:
			  ptr = &((struct sockaddr_in6 *) rp->ai_addr)->sin6_addr;
			  break;
		  }
		  inet_ntop(rp->ai_family, ptr, buff, rp->ai_addrlen);
		  printf("%s\n", buff);	
  }
