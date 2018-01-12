#!/usr/bin/python
import boto3

def list_buckets():
	bucket_list=[]
	s3 = boto3.resource('s3')
	buckets_all = s3.buckets.all()
	for b in s3.buckets.all():
		bucket_list.append(b.name)
	print bucket_list
	return bucket_list



def checkacl(bl):
	s3client=boto3.client('s3')
	url=""
	for b in bl:
		bacl=s3client.get_bucket_acl(Bucket=b)
		grantslist = bacl['Grants']
		for grante in grantslist:
			grantelist = grante['Grantee']
			if 'URI' in grantelist:
				url = grantelist['URI']
				print url
		if url == 'http://acs.amazonaws.com/groups/global/AllUsers':
			print '%s Bucket has public access Please check the access required or not' %(b)
		else:
			print "%s Bucket is Safe Public access is not enabled" %(b)

bl = list_buckets()
checkacl(bl)