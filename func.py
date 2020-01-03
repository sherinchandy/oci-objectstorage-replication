import io
import json
import oci

def handler(ctx, data: io.BytesIO = None):

    signer = oci.auth.signers.get_resource_principals_signer()
    client = oci.object_storage.ObjectStorageClient(config={}, signer=signer)

    body = json.loads(data.getvalue())
    event = body.get("eventType")
    jsonData = body.get("data")
    nameSpaceData = jsonData.get("additionalDetails")
    nameSpace = nameSpaceData.get("namespace")
    bucketName = nameSpaceData.get("bucketName")
    objectName = jsonData.get("resourceName")

    ## User Inputs target Object Storage Bucket and Region names.
    repBucket = "veloopra1"          # Provide your target bucket name here
    repRegion = "us-ashburn-1"       # provide your target bucket's region name here

    copy_obj_details = oci.object_storage.models.CopyObjectDetails(source_object_name=objectName,
                                                                   destination_region=repRegion,
                                                                   destination_namespace=nameSpace,
                                                                   destination_bucket=repBucket,
                                                                   destination_object_name=objectName)

    try:

        if (event == "com.oraclecloud.objectstorage.createobject"):
            RepObj = client.copy_object(nameSpace,bucketName,copy_obj_details)

        elif (event == "com.oraclecloud.objectstorage.deleteobject"):
            client.base_client.set_region(repRegion)
            RepObj = client.delete_object(nameSpace,repBucket,objectName)

        return RepObj

    except Exception as e:
        print(e)

