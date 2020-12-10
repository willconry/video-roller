import cv2
import numpy as np

def main():

    cap = cv2.VideoCapture('oz.MOV')
    # fps = cap.get(cv2.CAP_PROP_FPS)
    fps = 30
    
    ret, frame = cap.read()

    height, width, layers = frame.shape
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi',fourcc, fps, (width, height))

    n = 270
    vbuff = np.full((n, height, width, layers), np.uint8(0))
    fbuff = np.full((height, width, layers), np.uint8(0))

    fNo = 0 ; f0 = fNo % n
    while(cap.isOpened()):

        if ret == True:

            vbuff[f0] = frame

            for div in range(n):
                start = int(div*height/n)
                end = int((div+1)*height/n)
                fbuff[start:end,:,:] = vbuff[(f0-div)%n,start:end,:,:]

            out.write(fbuff)
            cv2.imshow('movie',fbuff)

            ret, frame = cap.read()

            fNo = fNo + 1 ; f0 = fNo % n

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            
            for _ in range(n):

                vbuff[f0] = np.full((height, width, layers), np.uint8(0))

                for div in range(n):

                    start = int(div*height/n)
                    end = int((div+1)*height/n)
                    fbuff[start:end,:,:] = vbuff[(f0-div)%n,start:end,:,:]

                out.write(fbuff)
                cv2.imshow('movie',fbuff)

                fNo = fNo + 1 ; f0 = fNo % n

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()