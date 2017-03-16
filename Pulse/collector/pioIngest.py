import predictionio, os
import numpy as np

if __name__ == "__main__":
    client = predictionio.EventClient(
        access_key=os.getenv('APP_ACCESS_KEY'),
        url=os.getenv('PIO_SERVER'),
        threads=5,
        qsize=500
    )

    data = np.genfromtxt('../data/db_host_cpu_usage.csv', delimiter=',')
    num = data.shape[0]
    # Set the 4 properties for a user
    for i in range(0,num):
        client.create_event(
            event="cpu",
            entity_type="point",
            entity_id=i,
            properties={
                "attr0": data[i][1]
            }
        )
    print "Imported %s events." % num